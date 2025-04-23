#================================================================================
#
#   ╦═╗╔═╗╔═╗╦ ╦╦ ╔╦╗╔═╗
#   ╠╦╝║╣ ╚═╗║ ║║  ║ ╚═╗
#   ╩╚═╚═╝╚═╝╚═╝╩═╝╩ ╚═╝
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
#   results.py
#
#   Thread-safe results collection and summary report generation
#   for tracking sync operation outcomes.
#
#================================================================================


import threading
from typing import Dict

class MirrorResults:
    def __init__(self):
        self.results: Dict[str, bool] = {}
        self.lock = threading.Lock()

    def update(self, table_name: str, success: bool) -> None:
        with self.lock:
            self.results[table_name] = success

    def get_results(self) -> Dict[str, bool]:
        with self.lock:
            return self.results.copy()

    def generate_summary_report(self) -> str:
        if not self.results:
            return "No migration results available."
        
        success_count = sum(1 for success in self.results.values() if success)
        total_count = len(self.results)
        
        report = [
            "=== Migration Summary ===",
            f"Tables processed: {total_count}",
            f"Successfully mirrored: {success_count}",
            f"Failed tables: {total_count - success_count}"
        ]
        
        if total_count - success_count > 0:
            failed_tables = [table for table, success in self.results.items() if not success]
            report.append(f"Failed tables: {', '.join(failed_tables)}")
        
        return "\n".join(report)
    

