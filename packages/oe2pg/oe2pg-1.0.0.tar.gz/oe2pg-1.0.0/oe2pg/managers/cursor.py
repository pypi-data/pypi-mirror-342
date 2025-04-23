#================================================================================
#
#   ╔═╗╦ ╦╦═╗╔═╗╔═╗╦═╗
#   ║  ║ ║╠╦╝╚═╗║ ║╠╦╝
#   ╚═╝╚═╝╩╚═╚═╝╚═╝╩╚═
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
#   cursor.py
#
#   Thread-safe cursor management system that controls and monitors
#   concurrent database operations, preventing resource exhaustion and
#   tracking cursor usage statistics.
#
#================================================================================

import threading
import logging
import time
from typing import Dict


## 
#
#   I wish this wasn't necessary, but Openedge uses (IMO) an archaic locking model, so this mandates stricter cursor management. You can configure broader ranges for available
#       cursors, but this is a mostly working way to make sure we do not hit "No cursor available" errors, which under some circumstances land the affected table in the ignored_tables.
#
##

class CursorManager:
    def __init__(self, max_cursors: int):
        self.max_cursors = max_cursors
        self.semaphore = threading.Semaphore(max_cursors)
        self.active_cursors = {}
        self.lock = threading.Lock()
        self.cursor_id_counter = 0
        self.logger = logging.getLogger("CursorManager")
        self.cursor_stats = {
            'total_acquired': 0,
            'total_released': 0,
            'max_concurrent': 0,
            'acquisition_times': [],
            'hold_times': []
        }
        self.cursor_tracking = {}

    def acquire(self, description: str = "") -> int:
        start_time = time.time()
        acquired = self.semaphore.acquire(blocking=True, timeout=60)
        acquisition_time = time.time() - start_time
        
        if not acquired:
            self.log_active_cursors()
            raise TimeoutError(f"Could not acquire cursor slot for {description} after 60s timeout")
        
        with self.lock:
            self.cursor_id_counter += 1
            cursor_id = self.cursor_id_counter
            self.active_cursors[cursor_id] = {
                'description': description,
                'acquire_time': time.time(),
                'thread_id': threading.get_ident()
            }
            
            active_count = len(self.active_cursors)
            self.cursor_stats['total_acquired'] += 1
            self.cursor_stats['acquisition_times'].append(acquisition_time)
            self.cursor_stats['max_concurrent'] = max(self.cursor_stats['max_concurrent'], active_count)
            
            op_type = description.split('_')[0] if '_' in description else description
            if op_type not in self.cursor_tracking:
                self.cursor_tracking[op_type] = {
                    'count': 0, 'active': 0, 'max_active': 0, 'total_time': 0
                }
            self.cursor_tracking[op_type]['count'] += 1
            self.cursor_tracking[op_type]['active'] += 1
            self.cursor_tracking[op_type]['max_active'] = max(
                self.cursor_tracking[op_type]['max_active'], 
                self.cursor_tracking[op_type]['active']
            )
            
            self.logger.info(f"Acquired cursor {cursor_id} ({description}). Active: {active_count}/{self.max_cursors}")
            
            if active_count > self.max_cursors * 0.9:
                self.logger.warning(f"Near cursor limit: {active_count}/{self.max_cursors}")
                self.log_active_cursors()
                
            if active_count > self.max_cursors:
                self.logger.error(f"ERROR: Active cursor count ({active_count}) exceeds limit ({self.max_cursors})!")
                self.semaphore.release()
                raise RuntimeError(f"Cursor accounting error: count {active_count} exceeds limit {self.max_cursors}")
                
            return cursor_id

    def release(self, cursor_id: int, description: str = "") -> bool:
        with self.lock:
            if cursor_id not in self.active_cursors:
                self.logger.warning(f"Attempted to release unknown cursor {cursor_id} ({description})")
                return False
                
            cursor_info = self.active_cursors.pop(cursor_id)
            hold_time = time.time() - cursor_info['acquire_time']
            active_count = len(self.active_cursors)
            
            self.cursor_stats['total_released'] += 1
            self.cursor_stats['hold_times'].append(hold_time)
            
            op_type = cursor_info['description'].split('_')[0] if '_' in cursor_info['description'] else cursor_info['description']
            if op_type in self.cursor_tracking:
                self.cursor_tracking[op_type]['active'] -= 1
                self.cursor_tracking[op_type]['total_time'] += hold_time
            
            self.logger.info(f"Released cursor {cursor_id} ({cursor_info['description']}). " +
                          f"Active: {active_count}/{self.max_cursors}. " +
                          f"Held for: {hold_time:.2f}s")
        
        self.semaphore.release()
        return True

    def get_active_cursors(self) -> Dict[int, Dict]:
        with self.lock:
            return self.active_cursors.copy()
            
    def get_active_cursor_count(self) -> int:
        with self.lock:
            return len(self.active_cursors)
            
    def log_active_cursors(self):
        with self.lock:
            if self.active_cursors:
                self.logger.info(f"Currently active cursors ({len(self.active_cursors)}):")
                for cursor_id, info in self.active_cursors.items():
                    self.logger.info(f"  - Cursor {cursor_id}: {info['description']}, " +
                                 f"active for {time.time() - info['acquire_time']:.2f}s, " +
                                 f"thread: {info['thread_id']}")
            else:
                self.logger.info("No active cursors")
    
    def log_cursor_stats(self):
        with self.lock:
            avg_acquisition = sum(self.cursor_stats['acquisition_times']) / max(1, len(self.cursor_stats['acquisition_times']))
            avg_hold = sum(self.cursor_stats['hold_times']) / max(1, len(self.cursor_stats['hold_times']))
            
            self.logger.info("=== Cursor Usage Statistics ===")
            self.logger.info(f"Total acquired: {self.cursor_stats['total_acquired']}")
            self.logger.info(f"Total released: {self.cursor_stats['total_released']}")
            self.logger.info(f"Maximum concurrent: {self.cursor_stats['max_concurrent']}")
            self.logger.info(f"Average acquisition time: {avg_acquisition:.4f}s")
            self.logger.info(f"Average hold time: {avg_hold:.4f}s")
            self.logger.info("\nBy operation type:")
            
            for op_type, stats in self.cursor_tracking.items():
                avg_time = stats['total_time'] / max(1, stats['count'])
                self.logger.info(f"  {op_type}: count={stats['count']}, " +
                              f"max_active={stats['max_active']}, " +
                              f"avg_time={avg_time:.4f}s")

    def detect_cursor_leaks(self, timeout_seconds: int = 300):
        with self.lock:
            current_time = time.time()
            for cursor_id, info in list(self.active_cursors.items()):
                if current_time - info['acquire_time'] > timeout_seconds:
                    self.logger.warning(f"Potential cursor leak: Cursor {cursor_id} ({info['description']}) " +
                                     f"active for {int(current_time - info['acquire_time'])}s")