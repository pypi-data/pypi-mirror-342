#================================================================================
#
#   ╦  ╔═╗╔═╗╔═╗╔═╗╦═╗
#   ║  ║ ║║ ╦║ ╦║╣ ╠╦╝
#   ╩═╝╚═╝╚═╝╚═╝╚═╝╩╚═
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
#   logger.py
#
#   Centralized logging system that handles both file and console output
#   with support for progress indicators and thread-safe operations.
#
#================================================================================


import logging
import sys
import threading
from typing import Optional

class LoggingManager:
    def __init__(self, log_file: str, log_level: int = logging.INFO):
        self.log_file = log_file
        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.print_lock = threading.Lock()

    def log(self, message: str, level: int = logging.INFO, console: bool = True, 
            progress: bool = False, end: Optional[str] = "\n") -> None:
        with self.print_lock:
            if console:
                if progress:
                    print("\r" + " " * 100, end="\r")
                    print(message, end=end)
                else:
                    print(message, end=end)
                sys.stdout.flush()
            
            if not progress or end != "\r":
                logging.log(level, message.strip() if progress else message)

    def format_time(self, seconds: float) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"