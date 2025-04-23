#================================================================================
#
#   ▄████▄   ██▓     ██▓
#  ▒██▀ ▀█  ▓██▒    ▓██▒
#  ▒▓█    ▄ ▒██░    ▒██▒
#  ▒▓▓▄ ▄██▒▒██░    ░██░
#  ▒ ▓███▀ ░░██████▒░██░
#  ░ ░▒ ▒  ░░ ▒░▓  ░░▓  
#    ░  ▒   ░ ░ ▒  ░ ▒ ░
#  ░          ░ ░    ▒ ░
#  ░ ░          ░  ░ ░  
#  ░                    
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
#   cli.py
#
#   Command-line interface module providing argument parsing, user interaction,
#   and proper error handling for the database mirroring tool.
#
#================================================================================


import argparse
import time
import sys
import logging
from datetime import datetime

from .core.mirror import DBMirror
from .core.config import Config
from .core.exceptions import MirrorError

def setup_logging(config):
    log_level = config.get_mirror_config().get('log_level', 'INFO')
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    log_file = config.get_mirror_config()['log_file']
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

def main():
    parser = argparse.ArgumentParser(
        description="OE2PG - Progress to PostgreSQL synchronization tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  oe2pg --config config.json --first-run                # Initial setup with schema creation
  oe2pg --config config.json                            # Regular synchronization
  oe2pg --config config.json --tables customer,orders   # Sync specific tables
  oe2pg --config config.json --repair                   # Repair discrepancies
  oe2pg --config config.json --prefer-timestamp         # Prefer timestamp-based sync when available
        """
    )
    
    parser.add_argument("--config", required=True, help="Path to configuration file")
    parser.add_argument("--first-run", action="store_true", help="First run mode to create tables")
    parser.add_argument("--tables", help="Comma-separated list of tables to sync")
    parser.add_argument("--repair", action="store_true", help="Repair row count discrepancies")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--silent", action="store_true", help="Suppress console output (for cron)")
    parser.add_argument("--prefer-timestamp", action="store_true", help="Prefer timestamp-based syncing when available")
    
    args = parser.parse_args()
    
    if not args.silent:
        print(f"\n=== DB Mirror - Started {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    try:
        config = Config(args.config)
        setup_logging(config)
        
        mirror = DBMirror(config, args.first_run, verbose=args.verbose, prefer_timestamp=args.prefer_timestamp)
        
        start_time = time.time()
        
        if args.repair:
            success = mirror.repair_all_discrepancies()
        else:
            tables = args.tables.split(',') if args.tables else None
            success = mirror.execute(specific_tables=tables)
            
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if not args.silent:
            print(f"\nTotal time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
            print(f"Status: {'SUCCESS' if success else 'FAILED'}")
            print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(1)
    except MirrorError as e:
        if not args.silent:
            print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        if not args.silent:
            print(f"Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)