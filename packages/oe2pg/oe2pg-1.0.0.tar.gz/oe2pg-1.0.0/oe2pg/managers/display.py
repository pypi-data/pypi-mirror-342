#================================================================================
#
#   ╔╦╗╦╔═╗╔═╗╦  ╔═╗╦ ╦
#    ║║║╚═╗╠═╝║  ╠═╣╚╦╝
#   ═╩╝╩╚═╝╩  ╩═╝╩ ╩ ╩ 
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
#   display.py
#
#   User interface display manager that provides real-time progress
#   visualization, status updates, and comprehensive summary reports.
#
#================================================================================


import time
from typing import Dict

class DisplayManager:
    def __init__(self, logger, tracking_manager):
        self.logger = logger
        self.tracking = tracking_manager
        self.start_time = time.time()
        
    def display_table_header(self, table_info: Dict, current_index: int, total_tables: int):
        header = f"\n{'='*60}"
        header += f"\nTable {current_index}/{total_tables}: {table_info['schema']}.{table_info['name']}"
        header += f"\nSync Type: {table_info['sync_type'].upper()} | Rows: {table_info['row_count']:,}"
        header += f"\n{'='*60}"
        self.logger.log(header)
    
    def display_progress(self, schema: str, table_name: str, rows_processed: int, 
                        total_rows: int, batch_num: int = None):
        percent = (rows_processed / max(1, total_rows)) * 100
        bar_length = 30
        filled_length = int(bar_length * rows_processed / max(1, total_rows))
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        progress_text = f"\r{table_name}: [{bar}] {percent:.1f}% ({rows_processed:,}/{total_rows:,} rows)"
        
        if rows_processed >= total_rows:
            progress_text += " - Complete!"
        else:
            current_progress = self.tracking.get_current_progress(schema, table_name)
            if current_progress and current_progress.get('start_time'):
                elapsed_time = time.time() - current_progress['start_time'].timestamp()
                
                if rows_processed > 0:
                    actual_rate = rows_processed / elapsed_time
                    remaining_rows = total_rows - rows_processed
                    estimated_seconds = remaining_rows / actual_rate
                    
                    if rows_processed > total_rows * 0.1:  
                        recent_progress = rows_processed - (total_rows * 0.1)
                        recent_time = elapsed_time - (total_rows * 0.1 / actual_rate)
                        recent_rate = recent_progress / recent_time if recent_time > 0 else actual_rate
                        
                        adjusted_rate = (actual_rate * 0.7) + (recent_rate * 0.3)
                        estimated_seconds = remaining_rows / adjusted_rate
                    
                    estimated_seconds *= 1.15
                    
                    estimated_time = self.logger.format_time(estimated_seconds)
                    progress_text += f" - {estimated_time}"
        
        self.logger.log(progress_text, progress=True, end="")
        self.tracking.update_sync_progress(schema, table_name, rows_processed)
        
    def display_summary(self, results: Dict[str, bool]):
        total = len(results)
        successful = sum(1 for success in results.values() if success)
        failed = total - successful
        
        summary = f"\n\n{'='*60}"
        summary += f"\nSync Summary"
        summary += f"\n{'='*60}"
        summary += f"\nTotal Tables: {total}"
        summary += f"\nSuccessful: {successful}"
        summary += f"\nFailed: {failed}"
        
        if failed > 0:
            summary += f"\n\nFailed Tables:"
            for table, success in results.items():
                if not success:
                    summary += f"\n  - {table}"
        
        summary += f"\n{'='*60}\n"
        self.logger.log(summary)