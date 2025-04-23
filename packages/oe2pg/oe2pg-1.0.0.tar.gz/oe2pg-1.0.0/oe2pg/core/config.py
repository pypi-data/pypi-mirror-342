#================================================================================
#
#   ╔═╗╔═╗╔╗╔╔═╗╦╔═╗
#   ║  ║ ║║║║╠╣ ║║ ╦
#   ╚═╝╚═╝╝╚╝╚  ╩╚═╝
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
#   config.py
#
#   Configuration management module that loads, validates, and provides
#   access to the application settings from JSON configuration files.
#
#================================================================================

import json
import sys
from typing import Dict, Any

class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self._validate_config()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print(f"Error: {config_path} file not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {config_path} - {str(e)}")
            sys.exit(1)

    def _validate_config(self) -> None:
        required_sections = {
            'progress_db': ['host', 'port', 'db_name', 'user', 'password', 'schema', 'jar_file', 'driver_class'],
            'postgres_db': ['conn_string'],
            'mirror_settings': ['batch_size', 'max_workers', 'max_cursors', 'log_file']
        }
        for section, keys in required_sections.items():
            if section not in self.config:
                print(f"Error: Missing configuration section: {section}")
                sys.exit(1)
            missing = [key for key in keys if key not in self.config[section]]
            if missing:
                print(f"Error: Missing required keys in {section}: {', '.join(missing)}")
                sys.exit(1)

    def get_progress_config(self) -> Dict[str, Any]:
        return self.config['progress_db']

    def get_postgres_config(self) -> Dict[str, Any]:
        return self.config['postgres_db']

    def get_mirror_config(self) -> Dict[str, Any]:
        return self.config['mirror_settings']