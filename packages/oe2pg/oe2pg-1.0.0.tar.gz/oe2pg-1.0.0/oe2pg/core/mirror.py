#================================================================================
#
#   ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ 
#   ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
#   ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝
#   ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗
#   ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║
#   ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
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
#   mirror.py
#
#   Core mirroring engine that orchestrates the data transfer between
#   Progress OpenEdge and PostgreSQL databases with support for full sync,
#   delta sync, and checksum-based change detection.
#
#================================================================================

import logging
import traceback
from typing import Dict, List
import json
import xxhash

from ..connectors.progress import ProgressConnector
from ..connectors.postgres import PostgresConnector
from ..managers.checksum import ChecksumManager
from ..managers.cursor import CursorManager
from ..managers.logger import LoggingManager
from ..managers.tracking import TrackingManager
from ..managers.display import DisplayManager
from ..models.results import MirrorResults
from .exceptions import ConnectionError, SyncError

class DBMirror:
    def __init__(self, config, first_run: bool = False, verbose: bool = False):
        self.config = config
        self.first_run = first_run
        self.verbose = verbose
        self.progress_config = config.get_progress_config()
        self.postgres_config = config.get_postgres_config()
        self.mirror_config = config.get_mirror_config()
        
        self.logger = LoggingManager(self.mirror_config['log_file'])
        self.cursor_manager = CursorManager(self.mirror_config['max_cursors'])
        self.results = MirrorResults()
        
        self.checksum_manager = None 
        self.progress_conn = None
        self.postgres_conn = None
        self.tracking_manager = None
        self.display_manager = None
        
    def execute(self, specific_tables: List[str] = None) -> bool:
        try:
            if not self._establish_connections():
                return False
            
            self.tracking_manager = TrackingManager(self.postgres_conn, self.logger)
            self.display_manager = DisplayManager(self.logger, self.tracking_manager)

            self.checksum_manager = ChecksumManager(
                self.postgres_conn, 
                self.progress_conn, 
                self.logger,
                block_size=self.mirror_config.get('checksum_block_size', 10000)            
            )


            # Check for PostgreSQL tables, create if not exists.... 

            if not self.tracking_manager.create_tracking_schema():
                raise SyncError("Failed to create tracking schema")
            
            if not self.checksum_manager.create_checksum_tables():
                self.logger.log("Warning: Checksum tables could not be created", level=logging.WARNING)            
            
            if self.first_run:
                if not self._setup_schema():
                    return False
            
            # Business logic - how do we sync these systems?

            sync_plan = self._prepare_sync_plan(specific_tables)
            success = self._execute_sync_with_feedback(sync_plan)
            
            self.display_manager.display_summary(self.results.get_results())
            
            return success
            
        except Exception as e:
            self.logger.log(f"Sync failed: {str(e)}", level=logging.ERROR)
            if self.verbose:
                self.logger.log(traceback.format_exc(), level=logging.ERROR)
            return False
        finally:
            self._cleanup()
    
    def repair_all_discrepancies(self) -> bool:
        try:
            if not self._establish_connections():
                return False
            
            self.tracking_manager = TrackingManager(self.postgres_conn, self.logger)
            discrepancies = self.tracking_manager.get_discrepancies()
            
            if not discrepancies:
                self.logger.log("No discrepancies found!")
                return True
            
            total = len(discrepancies)
            self.logger.log(f"Found {total} tables with row count discrepancies")
            
            for i, (schema, table, prog_rows, pg_rows, discrepancy) in enumerate(discrepancies, 1):
                self.logger.log(f"Repairing table {i}/{total}: {schema}.{table} (discrepancy: {discrepancy})")
                
                pk_column = self.progress_conn.get_primary_key(schema, table)
                
                if not pk_column:
                    self.logger.log(f"No primary key found for {schema}.{table}, performing full mirror")
                    self._perform_full_sync({'schema': schema, 'name': table, 'exists': True})
                elif pg_rows > prog_rows:
                    self.logger.log(f"Postgres has more rows than Progress - deduplicating {schema}.{table}")
                    self.postgres_conn.deduplicate_table(schema, table, pk_column)
                else:
                    self.logger.log(f"Progress has more rows than Postgres - performing full mirror for {schema}.{table}")
                    self._perform_full_sync({'schema': schema, 'name': table, 'exists': True})
            
            self.logger.log("Completed repair of all tables with discrepancies")
            return True
            
        except Exception as e:
            self.logger.log(f"Error repairing discrepancies: {str(e)}", level=logging.ERROR)
            if self.verbose:
                self.logger.log(traceback.format_exc(), level=logging.ERROR)
            return False
        finally:
            self._cleanup()
    
    def _establish_connections(self) -> bool:
        pool_min = self.postgres_config.get('pool_min_conn', 3)
        pool_max = self.postgres_config.get('pool_max_conn', 10)
        
        self.postgres_conn = PostgresConnector(
            self.postgres_config['conn_string'], 
            self.logger,
            pool_min_conn=pool_min,
            pool_max_conn=pool_max
        )
        
        self.progress_conn = ProgressConnector(
            **self.progress_config, 
            cursor_manager=self.cursor_manager,
            logger=self.logger, 
            postgres_connector=self.postgres_conn
        )
        
        if not self.progress_conn.connect():
            raise ConnectionError("Failed to connect to Progress database")
            
        if not self.postgres_conn.connect():
            raise ConnectionError("Failed to connect to PostgreSQL database")
            
        return True
    
    def _setup_schema(self) -> bool:
        self.logger.log("Setting up schema (first run)...")
        tables = self.progress_conn.get_tables()
        success_count = 0
        
        for table in tables:
            columns = self.progress_conn.get_columns(table['schema'], table['name'])
            if not columns:
                self.logger.log(f"Skipping table {table['name']} - no columns found")
                continue
            
            self.logger.log(f"Creating table '{table['name']}'...")
            success = self.postgres_conn.create_table(table['name'], columns)
            
            if success:
                self.logger.log(f"✓ Created table '{table['name']}'")
                success_count += 1
            else:
                self.logger.log(f"✗ Failed to create table '{table['name']}'", level=logging.ERROR)
        
        self.logger.log(f"Schema setup complete. Created {success_count}/{len(tables)} tables.")
        return success_count > 0
    
    def _prepare_sync_plan(self, specific_tables: List[str] = None) -> List[Dict]:
        sync_plan = []
        tables = self.progress_conn.get_tables()
        
        if specific_tables:
            tables = [t for t in tables if t['name'] in specific_tables or f"{t['schema']}.{t['name']}" in specific_tables]
        
        for table in tables:
            schema, name = table['schema'], table['name']
            
            if self.tracking_manager.is_table_ignored(schema, name):
                continue
            
            progress_count = self.progress_conn.get_row_count(schema, name)
            if progress_count == -1:
                continue
            
            postgres_count = 0
            table_exists = self.postgres_conn.table_exists(name)
            
            if table_exists:
                postgres_count = self.postgres_conn.get_row_count(name)
                if postgres_count == -1:
                    postgres_count = 0
            
            self.postgres_conn.upsert_row_count(schema, name, progress_count, postgres_count)
            
            sync_type = self._determine_sync_type(schema, name, progress_count, postgres_count, table_exists)
            
            if sync_type != 'none':
                sync_plan.append({
                    'schema': schema,
                    'name': name,
                    'sync_type': sync_type,
                    'row_count': progress_count,
                    'exists': table_exists
                })
        
        sync_plan.sort(key=lambda x: x['row_count'])
        
        return sync_plan
    
    def _determine_sync_type(self, schema: str, name: str, progress_count: int, 
                            postgres_count: int, table_exists: bool) -> str:
        """Enhanced sync type determination with timestamp support."""
        if not table_exists or postgres_count == 0:
            return 'full'
        
        if progress_count < 3000:
            return 'full'
        
        timestamp_columns = self.progress_conn.get_timestamp_columns(schema, name)
        timestamp_state = None
        
        if timestamp_columns:
            update_columns = [col for col in timestamp_columns if any(
                
                # I'm including this to "generalize" the script, in practice, with known tables, I'd use exact table names ..
                pattern in col.lower() for pattern in ['update', 'modified', 'changed', 'edit']
            )]
            
            ts_column = update_columns[0] if update_columns else timestamp_columns[0]
            timestamp_state = self.tracking_manager.get_timestamp_state(schema, name)
            
            if timestamp_state:
                return 'timestamp'
            else:
                latest_ts = self.progress_conn.get_latest_timestamp(schema, name, ts_column)
                if latest_ts:
                    self.tracking_manager.update_timestamp_state(schema, name, ts_column, latest_ts)
                    return 'full'  
        
        if self.checksum_manager and progress_count > self.mirror_config.get('checksum_threshold', 10000):
            if progress_count == postgres_count:
                changed_blocks = self.checksum_manager.detect_changed_blocks(schema, name)
                if changed_blocks:
                    return 'block' 
                else:
                    return 'none'
            else:
                delta_state = self.tracking_manager.get_delta_state(schema, name)
                if delta_state and delta_state['pk_column']:
                    return 'delta'
        
        return 'full'
    
    def _execute_sync_with_feedback(self, sync_plan: List[Dict]) -> bool:
        total_tables = len(sync_plan)
        success_overall = True
        
        for index, table_info in enumerate(sync_plan, 1):
            self.display_manager.display_table_header(table_info, index, total_tables)
            
            try:
                self.tracking_manager.start_table_sync(
                    table_info['schema'], 
                    table_info['name'], 
                    table_info['sync_type'], 
                    table_info['row_count']
                )
                
                if table_info['sync_type'] == 'full':
                    success = self._perform_full_sync(table_info)
                elif table_info['sync_type'] == 'delta':
                    success = self._perform_delta_sync(table_info)
                elif table_info['sync_type'] == 'block':
                    success = self._perform_block_sync(table_info)
                elif table_info['sync_type'] == 'timestamp':
                    success = self._perform_timestamp_sync(table_info)
                        
                self.tracking_manager.complete_table_sync(
                    table_info['schema'], 
                    table_info['name'],
                    'success' if success else 'failed'
                )
                
                self.results.update(f"{table_info['schema']}.{table_info['name']}", success)
                
                if not success:
                    success_overall = False
                    
            except Exception as e:
                if self._is_auth_error(e):
                    self._handle_auth_error(table_info, e)
                else:
                    self.logger.log(f"Error syncing {table_info['name']}: {str(e)}", level=logging.ERROR)
                    self.tracking_manager.complete_table_sync(
                        table_info['schema'], 
                        table_info['name'],
                        'failed',
                        str(e)
                    )
                self.results.update(f"{table_info['schema']}.{table_info['name']}", False)
                success_overall = False
        
        return success_overall
    
    # Start anew. As with the checksum method, use this only with a first run or with small tables as it's usually a LONG process.
    
    def _perform_full_sync(self, table_info: Dict) -> bool:
        schema, name = table_info['schema'], table_info['name']
        
        self.logger.log(f"Starting full sync for {schema}.{name}...")
        
        columns = self.progress_conn.get_columns(schema, name)
        column_names = [col['name'] for col in columns]
        
        if table_info['exists']:
            self.logger.log(f"Truncating existing table {name}...")
            if not self.postgres_conn.truncate_table(name):
                return False
        
        def progress_callback(batch, batch_num, total_batches, current_rows, total_rows, estimated_time):
            self.postgres_conn.insert_data(name, column_names, batch, batch_num, total_batches, current_rows, total_rows, estimated_time)
            self.display_manager.display_progress(schema, name, current_rows, total_rows, batch_num)
        
        total_rows = self.progress_conn.fetch_data(
            schema, name, column_names, 
            self.mirror_config['batch_size'], 
            progress_callback
        )
        
        if total_rows >= 0:
            self.postgres_conn.upsert_row_count(schema, name, total_rows, total_rows)
            
            pk_column = self.progress_conn.get_primary_key(schema, name)
            if pk_column and total_rows > 0:
                last_row = self.progress_conn.get_last_row(schema, name, pk_column)
                if last_row:
                    checksum = self._compute_row_checksum(last_row)
                    self.tracking_manager.update_delta_state(
                        schema, name, pk_column, 
                        str(last_row[0]), checksum, total_rows
                    )
            
            self.logger.log(f"✓ Completed full sync for {schema}.{name} - {total_rows:,} rows")
            return True
        else:
            self.logger.log(f"✗ Failed full sync for {schema}.{name}", level=logging.ERROR)
            return False
    
    # Default changed rows synchronization 

    def _perform_delta_sync(self, table_info: Dict) -> bool:
        schema, name = table_info['schema'], table_info['name']
        
        self.logger.log(f"Starting delta sync for {schema}.{name}...")
        
        delta_state = self.tracking_manager.get_delta_state(schema, name)
        if not delta_state:
            return self._perform_full_sync(table_info)
        
        columns = self.progress_conn.get_columns(schema, name)
        column_names = [col['name'] for col in columns]
        
        new_records = self.progress_conn.get_records_since_pk(
            schema, name, delta_state['pk_column'], delta_state['last_pk_value']
        )
        
        if not new_records:
            self.logger.log(f"No new records found for {schema}.{name}")
            return True
        
        processed = 0
        batch_size = self.mirror_config['batch_size']
        
        for i in range(0, len(new_records), batch_size):
            batch = new_records[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(new_records) + batch_size - 1) // batch_size
            
            if self.postgres_conn.insert_data(name, column_names, batch, batch_num, total_batches, processed + len(batch), len(new_records), ""):
                processed += len(batch)
                self.display_manager.display_progress(schema, name, processed, len(new_records))
        
        if processed > 0 and new_records:
            last_record = new_records[-1]
            checksum = self._compute_row_checksum(last_record)
            row_count = self.progress_conn.get_row_count(schema, name)
            self.tracking_manager.update_delta_state(
                schema, name, delta_state['pk_column'], 
                str(last_record[0]), checksum, row_count
            )
        
        if processed == len(new_records):
            self.logger.log(f"✓ Completed delta sync for {schema}.{name} - {processed:,} new rows")
            return True
        else:
            self.logger.log(f"✗ Failed delta sync for {schema}.{name}", level=logging.ERROR)
            return False

    # Assuming there are useful date or datetimestamp columns, we reference those to figure out where we left off.
       
    def _perform_timestamp_sync(self, table_info: Dict) -> bool:
        schema, name = table_info['schema'], table_info['name']
        
        self.logger.log(f"Starting timestamp-based sync for {schema}.{name}...")
        
        timestamp_state = self.tracking_manager.get_timestamp_state(schema, name)
        if not timestamp_state:
            return self._perform_full_sync(table_info)
        
        ts_column = timestamp_state['timestamp_column']
        last_timestamp = timestamp_state['last_timestamp']
        
        self.logger.log(f"Syncing changes since {last_timestamp} using column {ts_column}")
        
        columns = self.progress_conn.get_columns(schema, name)
        column_names = [col['name'] for col in columns]
        
        row_count = self.progress_conn.fetch_data_since_timestamp(
            schema, name, column_names, ts_column, last_timestamp,
            self.mirror_config['batch_size'],
            lambda batch, batch_num, total_batches, current_rows, total_rows, estimated_time: 
                self.postgres_conn.insert_data(
                    name, column_names, batch, batch_num, total_batches, 
                    current_rows, total_rows, estimated_time
                )
        )
        
        if row_count > 0:
            latest_ts = self.progress_conn.get_latest_timestamp(schema, name, ts_column)
            if latest_ts and latest_ts != last_timestamp:
                self.tracking_manager.update_timestamp_state(schema, name, ts_column, latest_ts)
                
            self.logger.log(f"✓ Completed timestamp sync for {schema}.{name} - {row_count:,} updated rows")
            return True
        else:
            self.logger.log(f"No changes found for {schema}.{name} since {last_timestamp}")
            return True
    
    # This synchronization is for the checksum based approach. Use with caution as it EATS RAM. 

    def _perform_block_sync(self, table_info: Dict) -> bool:
        schema, name = table_info['schema'], table_info['name']
        
        self.logger.log(f"Starting block sync for {schema}.{name}...")
        
        success = self.checksum_manager.sync_changed_blocks(schema, name, self)
        
        if success:
            self.logger.log(f"✓ Completed block sync for {schema}.{name}")
        else:
            self.logger.log(f"✗ Failed block sync for {schema}.{name}", level=logging.ERROR)
        
        return success
    
    def _is_auth_error(self, error: Exception) -> bool:
        auth_terms = ['permission denied', 'access denied', 'not authorized', 'insufficient privileges']
        return any(term in str(error).lower() for term in auth_terms)
    
    def _handle_auth_error(self, table_info: Dict, error: Exception):
        self.logger.log(f"Authorization error for {table_info['schema']}.{table_info['name']}: {str(error)}")
        self.tracking_manager.add_to_ignore_list(
            table_info['schema'], 
            table_info['name'], 
            f"Auth error: {str(error)}"
        )
    
    def _compute_row_checksum(self, row: List) -> str:
        row_str = json.dumps(row, sort_keys=True, default=str)
        hasher = xxhash.xxh64()
        hasher.update(row_str.encode())
        return hasher.hexdigest()

    def compute_all_checksums(self) -> bool:
        try:
            tables = self.progress_conn.get_tables()
            success_count = 0
            
            for table in tables:
                schema, name = table['schema'], table['name']
                
                if self.tracking_manager.is_table_ignored(schema, name):
                    continue
                
                self.logger.log(f"\nComputing checksums for {schema}.{name}...")
                
                if self.checksum_manager.update_block_checksums(schema, name):
                    success_count += 1
                else:
                    self.logger.log(f"Failed to compute checksums for {schema}.{name}", level=logging.ERROR)
            
            self.logger.log(f"\nCompleted checksum computation for {success_count} tables")
            return True
            
        except Exception as e:
            self.logger.log(f"Error in compute_all_checksums: {str(e)}", level=logging.ERROR)
            return False


    def _cleanup(self):
        if self.progress_conn:
            self.progress_conn.disconnect()
        if self.postgres_conn:
            self.postgres_conn.disconnect()
        
        self.cursor_manager.log_cursor_stats()