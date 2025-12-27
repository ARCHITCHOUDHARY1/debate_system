#log in
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class DebateLogger:
    def __init__(self, log_file: Optional[str] = None):
        self.logs: List[Dict[str, Any]] = []
        
        # Use provided log_file or default from config
        if log_file:
            self.log_file = log_file
        else:
            try:
                from config import LOG_FILE
                self.log_file = LOG_FILE
            except:
                self.log_file = "debate_log.jsonl"
        
        # Ensure log directory exists
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Initialize log file (start fresh for each debate session)
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                pass  # Create empty file
        except Exception as e:
            print(f"Warning: Could not initialize log file: {str(e)}")
    
    def log(self, event_type: str, data: Dict[str, Any]) -> None:
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "data": data
            }
            self.logs.append(log_entry)
            
            # Write immediately to file (JSON-lines format)
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            except Exception as file_error:
                print(f"Warning: Could not write log to file: {str(file_error)}")
            
            # Console logging (optional)
            try:
                from config import ENABLE_CONSOLE_LOGGING
                if ENABLE_CONSOLE_LOGGING:
                    print(f"[{event_type}] {data}")
            except (ImportError, Exception):
                pass  # Skip console logging if config not available
                
        except Exception as e:
            print(f"Logging error: {str(e)}")
    
    def save(self) -> None:
        try:
            print(f"\nLogs written to {self.log_file}")
            print(f"Total events logged: {len(self.logs)}")
        except Exception as e:
            print(f"Error in save: {str(e)}")
    
    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs
    
    def set_log_file(self, log_file: str) -> None:
        self.log_file = log_file
        
        # Ensure directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)


# Global logger instance
logger = DebateLogger()