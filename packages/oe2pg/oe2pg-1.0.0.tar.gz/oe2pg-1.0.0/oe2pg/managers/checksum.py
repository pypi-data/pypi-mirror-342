#================================================================================
#
#   ╔═╗╦ ╦╔═╗╔═╗╦╔═╔═╗╦ ╦╔╦╗
#   ║  ╠═╣║╣ ║  ╠╩╗╚═╗║ ║║║║
#   ╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╚═╝╩ ╩
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
#   checksum.py
#
#   Block-based checksum system for detecting changes in large tables
#   efficiently, enabling targeted synchronization of modified data blocks.
#
#================================================================================

import xxhash
import json
import logging
from typing import List, Tuple
import psycopg2

class ChecksumManager:
    def __init__(self, postgres_connector, progress_connector, logger, block_size=10000):
        self.postgres = postgres_connector
        self.progress = progress_connector
        self.logger = logger
        self.block_size = block_size
    
    def create_checksum_tables(self) -> bool:
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.checksum_state (
                    schema_name TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    pk_column TEXT NOT NULL,
                    total_rows BIGINT,
                    block_size INTEGER DEFAULT 10000,
                    last_full_checksum TEXT,
                    last_full_checksum_time TIMESTAMPTZ,
                    high_water_mark TEXT,
                    last_block_checksum TEXT,
                    last_check_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking.block_checksums (
                    schema_name TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    block_number INTEGER NOT NULL,
                    block_start_pk TEXT NOT NULL,
                    block_end_pk TEXT NOT NULL,
                    block_checksum TEXT NOT NULL,
                    row_count INTEGER,
                    computed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (schema_name, table_name, block_number)
                )
            """)
            
            return True
        except Exception as e:
            self.logger.log(f"Error creating checksum tables: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def compute_block_checksum(self, schema: str, table_name: str, pk_column: str, 
                             block_start: str, block_end: str) -> Tuple[str, int]:
        def compute_operation(cursor):
            query = f"""
                SELECT * FROM "{schema}"."{table_name}"
                WHERE "{pk_column}" >= ? AND "{pk_column}" < ?
                ORDER BY "{pk_column}"
            """
            cursor.execute(query, (block_start, block_end))
            
            hasher = xxhash.xxh64()
            row_count = 0
            
            while True:
                rows = cursor.fetchmany(1000)
                if not rows:
                    break
                    
                for row in rows:
                    row_str = json.dumps(row, sort_keys=True, default=str)
                    hasher.update(row_str.encode())
                    row_count += 1
            
            return hasher.hexdigest(), row_count
        
        result = self.progress.execute_with_cursor(
            compute_operation, 
            f"block_checksum_{schema}_{table_name}_{block_start}_{block_end}"
        )
        return result if result else ("", 0)
    
    def update_block_checksums(self, schema: str, table_name: str) -> bool:
        try:
            pk_column = self.progress.get_primary_key(schema, table_name)
            if not pk_column:
                self.logger.log(f"No primary key for {schema}.{table_name} - cannot compute checksums")
                return False
                
            row_count = self.progress.get_row_count(schema, table_name)
            if row_count <= 0:
                return True 
            
            min_max = self.progress.get_min_max_pk(schema, table_name, pk_column)
            if not min_max:
                return False
                
            min_pk, max_pk = min_max
            blocks = []
            
            if row_count <= self.block_size:
                blocks.append((0, min_pk, str(int(max_pk) + 1) if isinstance(max_pk, (int, float)) else max_pk))
            else:
                if isinstance(min_pk, (int, float)):
                    step = (max_pk - min_pk) / (row_count / self.block_size)
                    current = min_pk
                    block_num = 0
                    
                    while current < max_pk:
                        next_boundary = current + step
                        blocks.append((block_num, str(current), str(next_boundary)))
                        current = next_boundary
                        block_num += 1
                else:
                    self.logger.log(f"Non-numeric PK for {schema}.{table_name} - using row-based blocks")
                    return False

            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            for block_num, start_pk, end_pk in blocks:
                checksum, count = self.compute_block_checksum(schema, table_name, pk_column, start_pk, end_pk)
                
                cursor.execute("""
                    INSERT INTO tracking.block_checksums 
                    (schema_name, table_name, block_number, block_start_pk, block_end_pk, 
                     block_checksum, row_count, computed_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (schema_name, table_name, block_number) DO UPDATE
                    SET block_start_pk = EXCLUDED.block_start_pk,
                        block_end_pk = EXCLUDED.block_end_pk,
                        block_checksum = EXCLUDED.block_checksum,
                        row_count = EXCLUDED.row_count,
                        computed_at = EXCLUDED.computed_at
                """, (schema, table_name, block_num, start_pk, end_pk, checksum, count))
            
            cursor.execute("""
                INSERT INTO tracking.checksum_state 
                (schema_name, table_name, pk_column, total_rows, block_size, 
                 high_water_mark, last_check_time)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (schema_name, table_name) DO UPDATE
                SET total_rows = EXCLUDED.total_rows,
                    high_water_mark = EXCLUDED.high_water_mark,
                    last_check_time = EXCLUDED.last_check_time
            """, (schema, table_name, pk_column, row_count, self.block_size, str(max_pk)))
            
            return True
            
        except Exception as e:
            self.logger.log(f"Error updating block checksums: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def detect_changed_blocks(self, schema: str, table_name: str) -> List[int]:
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT block_number, block_start_pk, block_end_pk, block_checksum
                FROM tracking.block_checksums
                WHERE schema_name = %s AND table_name = %s
                ORDER BY block_number
            """, (schema, table_name))
            
            stored_blocks = cursor.fetchall()
            changed_blocks = []
            
            for block_num, start_pk, end_pk, stored_checksum in stored_blocks:
                pk_column = self.progress.get_primary_key(schema, table_name)
                current_checksum, _ = self.compute_block_checksum(
                    schema, table_name, pk_column, start_pk, end_pk
                )
                
                if current_checksum != stored_checksum:
                    changed_blocks.append(block_num)
                    self.logger.log(f"Block {block_num} changed for {schema}.{table_name}")
            
            return changed_blocks
            
        except Exception as e:
            self.logger.log(f"Error detecting changed blocks: {str(e)}", level=logging.ERROR)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def sync_changed_blocks(self, schema: str, table_name: str, mirror) -> bool:
        changed_blocks = self.detect_changed_blocks(schema, table_name)
        
        if not changed_blocks:
            self.logger.log(f"No changes detected for {schema}.{table_name}")
            return True
        
        try:
            conn = psycopg2.connect(self.postgres.conn_string)
            conn.autocommit = True
            cursor = conn.cursor()
            
            pk_column = self.progress.get_primary_key(schema, table_name)
            columns = self.progress.get_columns(schema, table_name)
            column_names = [col['name'] for col in columns]
            
            for block_num in changed_blocks:
                cursor.execute("""
                    SELECT block_start_pk, block_end_pk
                    FROM tracking.block_checksums
                    WHERE schema_name = %s AND table_name = %s AND block_number = %s
                """, (schema, table_name, block_num))
                
                result = cursor.fetchone()
                if not result:
                    continue
                    
                start_pk, end_pk = result
                
                self.logger.log(f"Syncing block {block_num} for {schema}.{table_name}")
                
                def sync_block_operation(cursor):
                    delete_query = f"""
                        DELETE FROM "{table_name}"
                        WHERE "{pk_column}" >= %s AND "{pk_column}" < %s
                    """
                    cursor.execute(delete_query, (start_pk, end_pk))
                    
                    self.progress.fetch_data_range(
                        schema, table_name, column_names, pk_column,
                        start_pk, end_pk, self.block_size,
                        lambda batch, *args: self.postgres.insert_data(
                            table_name, column_names, batch, *args
                        )
                    )
                
                mirror._perform_block_sync(sync_block_operation)
            
            self.update_block_checksums(schema, table_name)
            
            return True
            
        except Exception as e:
            self.logger.log(f"Error syncing changed blocks: {str(e)}", level=logging.ERROR)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()