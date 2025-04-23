#================================================================================
#
#   ╔═╗╦═╗╔═╗╔═╗╦═╗╔═╗╔═╗╔═╗
#   ╠═╝╠╦╝║ ║║ ╦╠╦╝║╣ ╚═╗╚═╗
#   ╩  ╩╚═╚═╝╚═╝╩╚═╚═╝╚═╝╚═╝
#
#--------------------------------------------------------------------------------
#
#   Author:  Benjamin Cance (KC8BWS)
#   Email:   canceb@gmail.com
#   Date:    22-04-2025
#
#--------------------------------------------------------------------------------
#
#   OE2PG Database Mirroring Tool
#   progress.py
#
#   Progress OpenEdge database connector that provides read-only access
#   to the source database, including table metadata, row counts, and
#   efficient batch data retrieval.
#
#================================================================================


import logging
import threading
import psycopg2
from typing import List, Dict, Any, Optional
from logger import LoggingManager

class PostgresConnector:
    def __init__(self, conn_string: str, logger: LoggingManager):
        self.conn_string = conn_string
        self.logger = logger
        self.connection = None
        self.connections = {}
        self.conn_lock = threading.Lock()

    def connect(self) -> bool:
        try:
            self.logger.log("Connecting to PostgreSQL...", end="")
            self.connection = psycopg2.connect(self.conn_string)
            self.connection.autocommit = True  # Set autocommit by default
            self.logger.log(" Connected!")
            return True
        except Exception as e:
            self.logger.log(f" Failed!\nPostgreSQL connection error: {str(e)}", level=logging.ERROR)
            return False

    def disconnect(self) -> None:
        if self.connection:
            try:
                self.logger.log("Disconnecting from PostgreSQL...", end="")
                self.connection.close()
                self.logger.log(" Done")
            except Exception as e:
                self.logger.log(f" Failed!\nPostgreSQL disconnect error: {str(e)}", level=logging.ERROR)
            finally:
                self.connection = None
        with self.conn_lock:
            for tid, conn in list(self.connections.items()):
                try:
                    conn.close()
                except Exception as e:
                    self.logger.log(f"Error closing connection for thread {tid}: {str(e)}", level=logging.ERROR)
            self.connections.clear()

    def get_connection(self) -> psycopg2.extensions.connection:
        thread_id = threading.get_ident()
        with self.conn_lock:
            if thread_id not in self.connections:
                # Create new connection with keepalive settings
                conn = psycopg2.connect(
                    self.conn_string,
                    connect_timeout=10,
                    keepalives=1,
                    keepalives_idle=30,
                    keepalives_interval=10
                )
                conn.autocommit = True
                self.connections[thread_id] = conn
            
            # Test if connection is still valid, recreate if needed
            conn = self.connections[thread_id]
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                # Reconnect if connection is dead
                self.logger.log("Reconnecting to PostgreSQL...", level=logging.INFO)
                try:
                    conn.close()
                except:
                    pass  # Ignore errors on close
                conn = psycopg2.connect(self.conn_string)
                conn.autocommit = True
                self.connections[thread_id] = conn
                
            return conn

    def create_tracking_schema(self) -> bool:
        cursor = None
        conn = None
        try:
            # Get a fresh connection with autocommit mode on
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Create schema
            cursor.execute("CREATE SCHEMA IF NOT EXISTS tracking")
            
            # Create tables one by one
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.row_counts (
                    schema_name TEXT,
                    table_name TEXT,
                    progress_rows BIGINT,
                    postgres_rows BIGINT,
                    discrepancy BIGINT,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.ignored_tables (
                    schema_name TEXT,
                    table_name TEXT,
                    reason TEXT,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.sync_jobs (
                    job_id SERIAL PRIMARY KEY,
                    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMPTZ,
                    status TEXT CHECK (status IN ('success', 'failure')),
                    tables_processed INTEGER,
                    tables_success INTEGER,
                    tables_failed INTEGER,
                    error_message TEXT
                )
            """)
            
            self.logger.log("Created tracking schema and tables in PostgreSQL")
            return True
        except Exception as e:
            self.logger.log(f"Error creating tracking schema: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def is_table_ignored(self, schema_name: str, table_name: str) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM tracking.ignored_tables 
                    WHERE schema_name = %s AND table_name = %s
                )
            """, (schema_name, table_name))
            
            exists = cursor.fetchone()[0]
            return exists
        except Exception as e:
            self.logger.log(f"Error checking ignored table {schema_name}.{table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def upsert_row_count(self, schema_name: str, table_name: str, progress_rows: int, postgres_rows: int) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            progress_rows_int = int(progress_rows) if progress_rows not in (-1, None) else 0
            postgres_rows_int = int(postgres_rows) if postgres_rows not in (-1, None) else 0
            discrepancy = progress_rows_int - postgres_rows_int
            
            cursor.execute("""
                INSERT INTO tracking.row_counts (schema_name, table_name, progress_rows, postgres_rows, discrepancy, timestamp)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (schema_name, table_name) DO UPDATE
                SET progress_rows = EXCLUDED.progress_rows,
                    postgres_rows = EXCLUDED.postgres_rows,
                    discrepancy = EXCLUDED.discrepancy,
                    timestamp = EXCLUDED.timestamp
            """, (schema_name, table_name, progress_rows_int, postgres_rows_int, discrepancy))
            
            self.logger.log(f"Upserted row count for {schema_name}.{table_name} into tracking.row_counts")
            return True
        except Exception as e:
            self.logger.log(f"Error upserting row count for {schema_name}.{table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def insert_ignored_table(self, schema_name: str, table_name: str, reason: str) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tracking.ignored_tables (schema_name, table_name, reason, timestamp)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (schema_name, table_name) DO UPDATE
                SET reason = EXCLUDED.reason,
                    timestamp = EXCLUDED.timestamp
            """, (schema_name, table_name, reason))
            
            self.logger.log(f"Upserted ignored table {schema_name}.{table_name} into tracking.ignored_tables")
            return True
        except Exception as e:
            self.logger.log(f"Error upserting ignored table {schema_name}.{table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def insert_sync_job(self, start_time: str, end_time: str, status: str, 
                       tables_processed: int, tables_success: int, tables_failed: int, 
                       error_message: Optional[str] = None) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tracking.sync_jobs 
                (start_time, end_time, status, tables_processed, tables_success, tables_failed, error_message)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (start_time, end_time, status, tables_processed, tables_success, tables_failed, error_message))
            
            self.logger.log(f"Inserted sync job record with status {status}")
            return True
        except Exception as e:
            self.logger.log(f"Error inserting sync job: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def map_to_postgres_type(self, progress_type: str) -> str:
        type_mapping = {
            'CHARACTER': 'TEXT',
            'VARCHAR': 'TEXT',
            'INTEGER': 'INTEGER',
            'DECIMAL': 'NUMERIC',
            'DATE': 'DATE',
            'DATETIME': 'TIMESTAMP',
            'LOGICAL': 'BOOLEAN'
        }
        return type_mapping.get(progress_type.upper(), 'TEXT')

    def create_table(self, table_name: str, columns: List[Dict[str, Any]]) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            column_defs = [f"\"{col['name']}\" {self.map_to_postgres_type(col['type'])}" for col in columns]
            create_query = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" ({', '.join(column_defs)})"
            cursor.execute(create_query)
            
            self.logger.log(f"Created table {table_name} in PostgreSQL")
            return True
        except Exception as e:
            self.logger.log(f"Error creating table {table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def truncate_table(self, table_name: str) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute(f"TRUNCATE TABLE \"{table_name}\"")
            
            self.logger.log(f"Truncated table {table_name}")
            return True
        except Exception as e:
            self.logger.log(f"Error truncating table {table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def table_exists(self, table_name: str) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (table_name.lower(),))
            
            exists = cursor.fetchone()[0]
            return exists
        except Exception as e:
            self.logger.log(f"Error checking table existence {table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def get_row_count(self, table_name: str) -> int:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
            count = cursor.fetchone()[0]
            
            return count
        except Exception as e:
            self.logger.log(f"Error getting row count for {table_name}: {str(e)}", level=logging.ERROR)
            return -1
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass

    def _display_progress(self, batch_num: int, total_batches: int, current_rows: int, 
                         total_rows: int, estimated_time: str):
        # Calculate percent complete
        percent = int((current_rows / max(1, total_rows)) * 100)
        
        # Create a progress bar
        bar_length = 30
        filled_length = int(bar_length * current_rows / max(1, total_rows))
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Format row counts with commas
        current_formatted = f"{current_rows:,}"
        total_formatted = f"{total_rows:,}"
        
        # Only show remaining time if we're not at 100%
        time_display = ""
        if current_rows < total_rows:
            time_display = f", {estimated_time} remaining"
        elif current_rows == total_rows and batch_num == total_batches:
            time_display = ", Complete!"
        else:
            # Handle case where rows are the same but batches aren't finished
            time_display = f", {estimated_time} remaining"
        
        # Clear line and show progress
        progress_text = f"\rBatch {batch_num}/{total_batches} [{bar}] {percent}% ({current_formatted}/{total_formatted} rows{time_display})"
        self.logger.log(progress_text, progress=True, end="")

    def insert_data(self, table_name: str, column_names: List[str], batch: List[Any], 
                    batch_num: int, total_batches: int, current_rows: int, total_rows: int, 
                    estimated_time: str, upsert: bool = False) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            columns = ", ".join([f"\"{col}\"" for col in column_names])
            placeholders = ", ".join(["%s" for _ in column_names])
            insert_query = f"INSERT INTO \"{table_name}\" ({columns}) VALUES ({placeholders})"
            
            cursor.executemany(insert_query, batch)
            
            # Use our improved progress display
            self._display_progress(batch_num, total_batches, current_rows, total_rows, estimated_time)
            return True
        except Exception as e:
            self.logger.log(f"Error inserting data: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
                    
    def deduplicate_table(self, schema_name: str, table_name: str, pk_column: str) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Log the start of deduplication
            self.logger.log(f"Deduplicating table {schema_name}.{table_name} using primary key {pk_column}")
            
            # Get original count
            cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
            original_count = cursor.fetchone()[0]
            
            # Create a temporary table with distinct rows
            cursor.execute(f"""
                CREATE TEMPORARY TABLE temp_{table_name} AS
                SELECT DISTINCT ON (\"{pk_column}\") *
                FROM \"{table_name}\"
            """)
            
            # Get deduplicated count
            cursor.execute(f"SELECT COUNT(*) FROM temp_{table_name}")
            distinct_count = cursor.fetchone()[0]
            
            # If there are duplicates, replace the original table
            if original_count > distinct_count:
                cursor.execute(f"TRUNCATE TABLE \"{table_name}\"")
                cursor.execute(f"""
                    INSERT INTO \"{table_name}\"
                    SELECT * FROM temp_{table_name}
                """)
                
                # Drop temporary table
                cursor.execute(f"DROP TABLE temp_{table_name}")
                
                # Update the row count tracking
                self.logger.log(f"Removed {original_count - distinct_count} duplicate rows from {table_name}")
                
                # Update row counts in tracking table
                progress_rows = self.progress.get_row_count(schema_name, table_name)
                self.upsert_row_count(schema_name, table_name, progress_rows, distinct_count)
                
                return True
            else:
                cursor.execute(f"DROP TABLE IF EXISTS temp_{table_name}")
                self.logger.log(f"No duplicates found in {table_name}")
                return True
        except Exception as e:
            self.logger.log(f"Error deduplicating table {table_name}: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass