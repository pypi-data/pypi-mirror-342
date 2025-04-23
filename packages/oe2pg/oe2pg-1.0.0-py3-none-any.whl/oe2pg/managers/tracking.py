#================================================================================
#
#   ╔╦╗╦═╗╔═╗╔═╗╦╔═╦╔╗╔╔═╗
#    ║ ╠╦╝╠═╣║  ╠╩╗║║║║║ ╦
#    ╩ ╩╚═╩ ╩╚═╝╩ ╩╩╝╚╝╚═╝
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
#   tracking.py
#
#   Manages synchronization state tracking including progress monitoring,
#   row count verification, delta state tracking, and ignored table management.
#
#================================================================================


from typing import Dict, Optional
import psycopg2
import logging

class TrackingManager:
    def __init__(self, postgres_connector, logger):
        self.postgres = postgres_connector
        self.logger = logger
        
    def create_tracking_schema(self) -> bool:
        cursor = None
        conn = None
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("CREATE SCHEMA IF NOT EXISTS tracking")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.sync_progress (
                    schema_name TEXT,
                    table_name TEXT,
                    sync_type TEXT CHECK (sync_type IN ('full', 'delta')),
                    rows_processed BIGINT DEFAULT 0,
                    total_rows BIGINT,
                    start_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMPTZ,
                    status TEXT CHECK (status IN ('running', 'success', 'failed')),
                    error_message TEXT,
                    PRIMARY KEY (schema_name, table_name, start_time)
                )
            """)
            
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
                CREATE TABLE IF NOT EXISTS tracking.delta_state (
                    schema_name TEXT,
                    table_name TEXT,
                    pk_column TEXT,
                    last_pk_value TEXT,
                    last_row_checksum TEXT,
                    rows_at_last_sync BIGINT,
                    last_sync_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.timestamp_state (
                    schema_name TEXT,
                    table_name TEXT,
                    timestamp_column TEXT,
                    last_timestamp TEXT,
                    last_sync_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name)
                )
            """)
            
            self.logger.log("Created tracking schema and tables")
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
    
    def start_table_sync(self, schema_name: str, table_name: str, sync_type: str, total_rows: int) -> bool:
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tracking.sync_progress 
                (schema_name, table_name, sync_type, total_rows, status)
                VALUES (%s, %s, %s, %s, 'running')
            """, (schema_name, table_name, sync_type, total_rows))
            
            return True
        except Exception as e:
            self.logger.log(f"Error starting sync tracking: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update_sync_progress(self, schema_name: str, table_name: str, rows_processed: int):
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                WITH running_sync AS (
                    SELECT schema_name, table_name, start_time 
                    FROM tracking.sync_progress
                    WHERE schema_name = %s AND table_name = %s 
                    AND status = 'running'
                    ORDER BY start_time DESC
                    LIMIT 1
                )
                UPDATE tracking.sync_progress
                SET rows_processed = %s
                FROM running_sync
                WHERE tracking.sync_progress.schema_name = running_sync.schema_name
                  AND tracking.sync_progress.table_name = running_sync.table_name
                  AND tracking.sync_progress.start_time = running_sync.start_time
            """, (schema_name, table_name, rows_processed))
            
        except Exception as e:
            self.logger.log(f"Error updating sync progress: {str(e)}", level=logging.ERROR)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def complete_table_sync(self, schema_name: str, table_name: str, status: str, error_message: str = None):
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                WITH running_sync AS (
                    SELECT schema_name, table_name, start_time 
                    FROM tracking.sync_progress
                    WHERE schema_name = %s AND table_name = %s 
                    AND status = 'running'
                    ORDER BY start_time DESC
                    LIMIT 1
                )
                UPDATE tracking.sync_progress
                SET status = %s, end_time = CURRENT_TIMESTAMP, error_message = %s
                FROM running_sync
                WHERE tracking.sync_progress.schema_name = running_sync.schema_name
                  AND tracking.sync_progress.table_name = running_sync.table_name
                  AND tracking.sync_progress.start_time = running_sync.start_time
            """, (schema_name, table_name, status, error_message))
            
        except Exception as e:
            self.logger.log(f"Error completing sync tracking: {str(e)}", level=logging.ERROR)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_current_progress(self, schema_name: str, table_name: str) -> Optional[Dict]:
        try:
            with self.postgres.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT sync_type, rows_processed, total_rows, start_time
                    FROM tracking.sync_progress
                    WHERE schema_name = %s AND table_name = %s 
                    AND status = 'running'
                    ORDER BY start_time DESC
                    LIMIT 1
                """, (schema_name, table_name))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'sync_type': result[0],
                        'rows_processed': result[1],
                        'total_rows': result[2],
                        'start_time': result[3]
                    }
                return None
        except Exception as e:
            self.logger.log(f"Error getting progress: {str(e)}", level=logging.ERROR)
            return None
        finally:
            if cursor:
                cursor.close()
    
    def add_to_ignore_list(self, schema_name: str, table_name: str, reason: str):
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tracking.ignored_tables (schema_name, table_name, reason, timestamp)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (schema_name, table_name) DO UPDATE
                SET reason = EXCLUDED.reason,
                    timestamp = EXCLUDED.timestamp
            """, (schema_name, table_name, reason))
            
            self.logger.log(f"Added {schema_name}.{table_name} to ignore list: {reason}")
        except Exception as e:
            self.logger.log(f"Error adding to ignore list: {str(e)}", level=logging.ERROR)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def is_table_ignored(self, schema_name: str, table_name: str) -> bool:
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM tracking.ignored_tables 
                    WHERE schema_name = %s AND table_name = %s
                )
            """, (schema_name, table_name))
            
            return cursor.fetchone()[0]
        except Exception as e:
            self.logger.log(f"Error checking ignored table: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_delta_state(self, schema_name: str, table_name: str) -> Optional[Dict]:
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT pk_column, last_pk_value, last_row_checksum, rows_at_last_sync
                FROM tracking.delta_state
                WHERE schema_name = %s AND table_name = %s
            """, (schema_name, table_name))
            
            result = cursor.fetchone()
            if result:
                return {
                    'pk_column': result[0],
                    'last_pk_value': result[1],
                    'last_row_checksum': result[2],
                    'rows_at_last_sync': result[3]
                }
            return None
        except Exception as e:
            self.logger.log(f"Error getting delta state: {str(e)}", level=logging.ERROR)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def update_delta_state(self, schema_name: str, table_name: str, pk_column: str, 
                          last_pk_value: str, last_row_checksum: str, row_count: int):
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO tracking.delta_state 
                (schema_name, table_name, pk_column, last_pk_value, last_row_checksum, rows_at_last_sync)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (schema_name, table_name) DO UPDATE
                SET pk_column = EXCLUDED.pk_column,
                    last_pk_value = EXCLUDED.last_pk_value,
                    last_row_checksum = EXCLUDED.last_row_checksum,
                    rows_at_last_sync = EXCLUDED.rows_at_last_sync,
                    last_sync_timestamp = CURRENT_TIMESTAMP
            """, (schema_name, table_name, pk_column, last_pk_value, last_row_checksum, row_count))
            
        except Exception as e:
            self.logger.log(f"Error updating delta state: {str(e)}", level=logging.ERROR)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def get_timestamp_state(self, schema_name: str, table_name: str) -> Optional[Dict]:
        try:
            with self.postgres.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT timestamp_column, last_timestamp, last_sync_timestamp
                    FROM tracking.timestamp_state
                    WHERE schema_name = %s AND table_name = %s
                """, (schema_name, table_name))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'timestamp_column': result[0],
                        'last_timestamp': result[1],
                        'last_sync_timestamp': result[2]
                    }
                return None
        except Exception as e:
            self.logger.log(f"Error getting timestamp state: {str(e)}", level=logging.ERROR)
            return None

    def update_timestamp_state(self, schema_name: str, table_name: str, 
                            timestamp_column: str, last_timestamp: str):
        try:
            with self.postgres.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO tracking.timestamp_state 
                    (schema_name, table_name, timestamp_column, last_timestamp, last_sync_timestamp)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (schema_name, table_name) DO UPDATE
                    SET timestamp_column = EXCLUDED.timestamp_column,
                        last_timestamp = EXCLUDED.last_timestamp,
                        last_sync_timestamp = EXCLUDED.last_sync_timestamp
                """, (schema_name, table_name, timestamp_column, last_timestamp))
                
                cursor.close()
                
        except Exception as e:
            self.logger.log(f"Error updating timestamp state: {str(e)}", level=logging.ERROR)





















