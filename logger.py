#log in
import json
from datetime import datetime
from typing import Any, Dict, List
from config import LOG_FILE, ENABLE_CONSOLE_LOGGING


class DebateLogger:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self.log_file = LOG_FILE
    
    def log(self, event_type: str, data: Dict[str, Any]) -> None:
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "data": data
            }
            self.logs.append(log_entry)
            
            if ENABLE_CONSOLE_LOGGING:
                print(f"[{event_type}] {data}")
        except Exception as e:
            print(f"Logging error: {str(e)}")
    
    def save(self) -> None:
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, indent=2, ensure_ascii=False)
            print(f"\nLogs saved to {self.log_file}")
        except Exception as e:
            print(f"Error saving logs: {str(e)}")
    
    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs


logger = DebateLogger()