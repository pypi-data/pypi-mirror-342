#================================================================================
#
#   ╦╔═╗╔╗╔╔═╗╦═╗╔═╗
#   ║║ ╦║║║║ ║╠╦╝║╣ 
#   ╩╚═╝╝╚╝╚═╝╩╚═╚═╝
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
#   ignore.py
#
#   Thread-safe ignore list management for tables that should be skipped
#   during synchronization due to access restrictions or user preferences.
#
#================================================================================

import os
import threading
from typing import Set

class IgnoreListManager:
    def __init__(self, ignore_file: str):
        self.ignore_file = ignore_file
        self.ignore_set: Set[str] = set()
        self.lock = threading.Lock()
        self.load_ignore_list()

    def load_ignore_list(self) -> None:
        if os.path.exists(self.ignore_file):
            with open(self.ignore_file, 'r') as f:
                self.ignore_set = {line.strip() for line in f if line.strip()}

    def add(self, table_name: str) -> None:
        with self.lock:
            self.ignore_set.add(table_name)
            with open(self.ignore_file, 'a') as f:
                f.write(f"{table_name}\n")

    def is_ignored(self, table_name: str) -> bool:
        return table_name in self.ignore_set

    def get_all(self) -> Set[str]:
        return self.ignore_set.copy()