#================================================================================
#
#   ╔═╗╔═╗╔═╗╔╦╗╔═╗╦═╗╔═╗╔═╗
#   ╠═╝║ ║╚═╗ ║ ║ ╦╠╦╝║╣ ╚═╗
#   ╩  ╚═╝╚═╝ ╩ ╚═╝╩╚═╚═╝╚═╝
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
#   postgres.py
#
#   PostgreSQL database connector that manages target database connections,
#   schema creation, data insertion, and tracking table operations.
#
#================================================================================


import logging
import time
from typing import List, Dict, Any, Optional
import jaydebeapi
from cursor import CursorManager
from logger import LoggingManager

class ProgressConnector:
    def __init__(self,  jar_file: str, driver_class: str, host: str, port: int, 
                 db_name: str, user: str, password: str, schema: str, 
                 cursor_manager: CursorManager, logger: LoggingManager, 
                 postgres_connector):
        self.jar_file = jar_file
        self.driver_class = driver_class
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password
        self.schema = schema
        self.connection = None
        self.cursor_manager = cursor_manager
        self.logger = logger
        self.postgres_connector = postgres_connector

    def connect(self) -> bool:
        try:
            self.logger.log(f"Connecting to Progress DB ({self.host}:{self.port})...", end="")
            jdbc_url = f"jdbc:datadirect:openedge://{self.host}:{self.port};databaseName={self.db_name};ReadOnly=true"
            self.connection = jaydebeapi.connect(
                self.driver_class, jdbc_url, [self.user, self.password], self.jar_file
            )
            try:
                if hasattr(self.connection, 'jconn'):
                    self.connection.jconn.setAutoCommit(False)
                    # Set read-only mode at connection level
                    if hasattr(self.connection.jconn, 'setReadOnly'):
                        self.connection.jconn.setReadOnly(True)
            except Exception as e:
                self.logger.log(f"Warning: Could not set connection properties: {e}", level=logging.WARNING)
            self.logger.log(" Connected in read-only mode!")
            return True
        except Exception as e:
            self.logger.log(f" Failed!\nConnection error: {str(e)}", level=logging.ERROR)
            return False

    def disconnect(self) -> None:
        if self.connection:
            try:
                self.logger.log("Disconnecting from Progress DB...", end="")
                self.connection.close()
                self.logger.log(" Done")
            except Exception as e:
                self.logger.log(f" Failed!\nProgress disconnect error: {str(e)}", level=logging.ERROR)
            finally:
                self.connection = None

    def execute_with_cursor(self, operation_func, description=""):
        if not self.connection:
            raise ConnectionError("Not connected to database")
        
        cursor = None
        cursor_id = None
        try:
            cursor_id = self.cursor_manager.acquire(description)
            cursor = self.connection.cursor()
            result = operation_func(cursor)
            self.connection.commit()
            return result
        except Exception as e:
            self.logger.log(f"Error in {description}: {str(e)}", level=logging.ERROR)
            try:
                if self.connection:
                    self.connection.rollback()
            except Exception as rollback_error:
                self.logger.log(f"Rollback error: {str(rollback_error)}", level=logging.ERROR)
            
            if "permission denied" in str(e).lower() or "access denied" in str(e).lower() or "not authorized" in str(e).lower():
                if description.startswith("get_") or description.startswith("count_") or description.startswith("fetch_"):
                    table_name = "_".join(description.split("_")[1:])
                    if table_name:
                        self.logger.log(f"Authorization error detected for {table_name}. Adding to tracking.ignored_tables.")
                        schema, table = table_name.split(".", 1) if "." in table_name else (self.schema, table_name)
                        self.postgres_connector.insert_ignored_table(schema, table, f"Authorization error: {str(e)}")
            return None
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as close_error:
                    self.logger.log(f"Error closing cursor: {str(close_error)}", level=logging.ERROR)
            if cursor_id:
                self.cursor_manager.release(cursor_id, description)

    def get_tables(self) -> List[Dict[str, str]]:
        def get_tables_operation(cursor):
            metadata = self.connection.jconn.getMetaData()
            result_set = metadata.getTables(None, self.schema, None, ["TABLE"])
            tables = []
            while result_set.next():
                schema_name = result_set.getString("TABLE_SCHEM")
                table_name = result_set.getString("TABLE_NAME")
                tables.append({"schema": schema_name, "name": table_name})
            return tables
        return self.execute_with_cursor(get_tables_operation, "get_tables") or []

    def get_columns(self, schema: str, table_name: str) -> List[Dict[str, Any]]:
        def get_columns_operation(cursor):
            metadata = self.connection.jconn.getMetaData()
            result_set = metadata.getColumns(None, schema, table_name, None)
            columns = []
            while result_set.next():
                column_name = result_set.getString("COLUMN_NAME")
                data_type = result_set.getString("TYPE_NAME")
                columns.append({"name": column_name, "type": data_type})
            return columns
        return self.execute_with_cursor(get_columns_operation, f"get_columns_{schema}_{table_name}") or []

    def get_primary_key(self, schema: str, table_name: str) -> Optional[str]:
        def get_pk_operation(cursor):
            metadata = self.connection.jconn.getMetaData()
            result_set = metadata.getPrimaryKeys(None, schema, table_name)
            pk_column = None
            while result_set.next():
                pk_column = result_set.getString("COLUMN_NAME")
                break
            return pk_column
        return self.execute_with_cursor(get_pk_operation, f"get_pk_{schema}_{table_name}")

    def get_row_count(self, schema: str, table_name: str) -> int:
        def count_operation(cursor):
            qualified_table = f"\"{schema}\".\"{table_name}\""
            cursor.execute(f"SELECT COUNT(*) FROM {qualified_table}")
            return cursor.fetchone()[0]
        result = self.execute_with_cursor(count_operation, f"count_{schema}_{table_name}")
        return result if result is not None else -1

    def get_min_max_pk(self, schema: str, table_name: str, pk_column: str) -> Optional[tuple]:
        def min_max_operation(cursor):
            qualified_table = f"\"{schema}\".\"{table_name}\""
            cursor.execute(f"SELECT MIN(\"{pk_column}\"), MAX(\"{pk_column}\") FROM {qualified_table}")
            result = cursor.fetchone()
            if result and result[0] is not None and result[1] is not None:
                return (result[0], result[1])
            return None
        return self.execute_with_cursor(min_max_operation, f"min_max_{schema}_{table_name}")

    def fetch_data(self, schema: str, table_name: str, column_names: List[str], 
                batch_size: int, callback: callable) -> int:
        def fetch_operation(cursor):
            start_time = time.time()
            total_rows = 0
            columns_str = ", ".join([f"\"{col}\"" for col in column_names])
            qualified_table = f"\"{schema}\".\"{table_name}\""
            
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {qualified_table}")
                estimated_total = cursor.fetchone()[0]
            except Exception as e:
                self.logger.log(f"Error getting row count: {str(e)}", level=logging.WARNING)
                estimated_total = 0
            
            cursor.execute(f"SELECT {columns_str} FROM {qualified_table}")
            batch_count = 0
            
            batch_times = []
            processing_times = []
            startup_time = time.time() - start_time
            
            while True:
                batch_start = time.time()
                batch = cursor.fetchmany(batch_size)
                fetch_time = time.time() - batch_start
                
                if not batch:
                    break
                    
                batch_count += 1
                process_start = time.time()
                total_rows += len(batch)
                
                if batch_count > 1:
                    batch_times.append(fetch_time)
                    processing_times.append(process_start - batch_start)
                    
                    recent_batch_times = batch_times[-10:]
                    recent_process_times = processing_times[-10:]
                    
                    avg_batch_time = sum(recent_batch_times) / len(recent_batch_times)
                    avg_process_time = sum(recent_process_times) / len(recent_process_times)
                    
                    total_time_per_batch = avg_batch_time + avg_process_time
                    remaining_batches = (estimated_total - total_rows) / batch_size
                    estimated_seconds = remaining_batches * total_time_per_batch
                    
                    estimated_seconds *= 1.1
                else:
                    elapsed_time = time.time() - start_time
                    rows_per_second = total_rows / max(0.1, elapsed_time)
                    remaining_rows = estimated_total - total_rows
                    estimated_seconds = remaining_rows / max(1, rows_per_second)
                
                estimated_time = self.logger.format_time(estimated_seconds)
                
                total_batches = (estimated_total + batch_size - 1) // batch_size if estimated_total > 0 else batch_count + 1
                callback(batch, batch_count, total_batches, total_rows, max(total_rows, estimated_total), estimated_time)
                
                process_end = time.time()
                processing_times.append(process_end - process_start)
            
            self.logger.log("")
            return total_rows
        
        result = self.execute_with_cursor(fetch_operation, f"fetch_{schema}_{table_name}")
        return result if result is not None else 0

    def fetch_data_range(self, schema: str, table_name: str, column_names: List[str],
                        pk_column: str, min_val: int, max_val: int, batch_size: int, 
                        callback: callable) -> int:
        def fetch_range_operation(cursor):
            start_time = time.time()
            total_rows = 0
            columns_str = ", ".join([f"\"{col}\"" for col in column_names])
            qualified_table = f"\"{schema}\".\"{table_name}\""
            
            cursor.execute(f"SELECT COUNT(*) FROM {qualified_table} WHERE \"{pk_column}\" >= ? AND \"{pk_column}\" < ?", 
                          (min_val, max_val))
            estimated_total = cursor.fetchone()[0]
            
            cursor.execute(f"""
                SELECT {columns_str} FROM {qualified_table} 
                WHERE \"{pk_column}\" >= ? AND \"{pk_column}\" < ?
                ORDER BY \"{pk_column}\"
            """, (min_val, max_val))
            
            batch_count = 0
            
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                    
                batch_count += 1
                total_rows += len(batch)
                elapsed_time = time.time() - start_time
                rows_per_second = total_rows / max(0.1, elapsed_time)
                
                remaining_rows = estimated_total - total_rows
                estimated_seconds = remaining_rows / max(1, rows_per_second)
                estimated_time = self.logger.format_time(estimated_seconds)
                
                callback(batch, batch_count, (estimated_total // batch_size) + 1, 
                        total_rows, estimated_total, estimated_time)
                
            return total_rows
        
        result = self.execute_with_cursor(fetch_range_operation, f"fetch_range_{schema}_{table_name}_{min_val}_{max_val}")
        return result if result is not None else 0
    
    def get_records_since_pk(self, schema: str, table_name: str, pk_column: str, last_pk_value: str) -> List[List]:
        """Get records where primary key is greater than given value."""
        def fetch_since_pk_operation(cursor):
            qualified_table = f"\"{schema}\".\"{table_name}\""
            
            query = f"""
                SELECT * FROM {qualified_table}
                WHERE \"{pk_column}\" > ?
                ORDER BY \"{pk_column}\" ASC
            """
            
            cursor.execute(query, (last_pk_value,))
            
            # Use fetchmany for memory efficiency
            results = []
            while True:
                batch = cursor.fetchmany(5000)
                if not batch:
                    break
                results.extend(batch)
            
            return results
        
        return self.execute_with_cursor(fetch_since_pk_operation, f"fetch_since_{schema}_{table_name}")

    def get_last_row(self, schema: str, table_name: str, pk_column: str) -> Optional[List]:
        """Get the last row from a table based on primary key."""
        def last_row_operation(cursor):
            qualified_table = f"\"{schema}\".\"{table_name}\""
            
            query = f"""
                SELECT * FROM {qualified_table}
                ORDER BY \"{pk_column}\" DESC
                FETCH FIRST 1 ROWS ONLY
            """
            
            cursor.execute(query)
            return cursor.fetchone()
        
        return self.execute_with_cursor(last_row_operation, f"last_row_{schema}_{table_name}")

    def get_timestamp_columns(self, schema: str, table_name: str) -> List[str]:
        def get_ts_columns_operation(cursor):
            metadata = self.connection.jconn.getMetaData()
            result_set = metadata.getColumns(None, schema, table_name, None)
            
            timestamp_columns = []
            while result_set.next():
                column_name = result_set.getString("COLUMN_NAME")
                data_type = result_set.getString("TYPE_NAME")
                
                if "DATE" in data_type.upper() or "TIME" in data_type.upper():
                    timestamp_columns.append(column_name)
                    
            return timestamp_columns
        
        return self.execute_with_cursor(get_ts_columns_operation, f"get_ts_cols_{schema}_{table_name}") or []

    def fetch_data_since_timestamp(self, schema: str, table_name: str, column_names: List[str], 
                                timestamp_column: str, last_timestamp: str, 
                                batch_size: int, callback: callable) -> int:
        def fetch_since_ts_operation(cursor):
            start_time = time.time()
            total_rows = 0
            columns_str = ", ".join([f"\"{col}\"" for col in column_names])
            qualified_table = f"\"{schema}\".\"{table_name}\""
            
            # Get estimated count for progress tracking
            count_query = f"""
                SELECT COUNT(*) FROM {qualified_table}
                WHERE \"{timestamp_column}\" > ?
            """
            cursor.execute(count_query, (last_timestamp,))
            estimated_total = cursor.fetchone()[0]
            
            # Fetch data
            query = f"""
                SELECT {columns_str} FROM {qualified_table}
                WHERE \"{timestamp_column}\" > ?
                ORDER BY \"{timestamp_column}\"
            """
            cursor.execute(query, (last_timestamp,))
            
            batch_count = 0
            batch_times = []
            processing_times = []
            
            while True:
                batch_start = time.time()
                batch = cursor.fetchmany(batch_size)
                fetch_time = time.time() - batch_start
                
                if not batch:
                    break
                    
                batch_count += 1
                process_start = time.time()
                total_rows += len(batch)
                
                # Calculate time estimates
                if batch_count > 1:
                    batch_times.append(fetch_time)
                    processing_times.append(process_start - batch_start)
                    
                    recent_batch_times = batch_times[-10:]
                    recent_process_times = processing_times[-10:]
                    
                    avg_batch_time = sum(recent_batch_times) / len(recent_batch_times)
                    avg_process_time = sum(recent_process_times) / len(recent_process_times)
                    
                    total_time_per_batch = avg_batch_time + avg_process_time
                    remaining_batches = (estimated_total - total_rows) / batch_size
                    estimated_seconds = remaining_batches * total_time_per_batch * 1.1
                else:
                    elapsed_time = time.time() - start_time
                    rows_per_second = total_rows / max(0.1, elapsed_time)
                    remaining_rows = estimated_total - total_rows
                    estimated_seconds = remaining_rows / max(1, rows_per_second)
                
                estimated_time = self.logger.format_time(estimated_seconds)
                total_batches = (estimated_total + batch_size - 1) // batch_size if estimated_total > 0 else batch_count + 1
                
                callback(batch, batch_count, total_batches, total_rows, max(total_rows, estimated_total), estimated_time)
                
                process_end = time.time()
                processing_times.append(process_end - process_start)
            
            return total_rows
        
        result = self.execute_with_cursor(fetch_since_ts_operation, f"fetch_since_ts_{schema}_{table_name}")
        return result if result is not None else 0

    def get_latest_timestamp(self, schema: str, table_name: str, timestamp_column: str) -> str:
        def get_latest_ts_operation(cursor):
            qualified_table = f"\"{schema}\".\"{table_name}\""
            query = f"""
                SELECT MAX(\"{timestamp_column}\") FROM {qualified_table}
            """
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result and result[0] else None
        
        return self.execute_with_cursor(get_latest_ts_operation, f"get_latest_ts_{schema}_{table_name}")





