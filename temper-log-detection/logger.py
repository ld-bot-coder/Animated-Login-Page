"""
Logging module for tamper events and system actions
"""
import pandas as pd
import os
from datetime import datetime
from config import TAMPER_LOG_FILE


class Logger:
    """Manages logging of tamper events and system actions"""
    
    def __init__(self):
        self.log_file = TAMPER_LOG_FILE
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.log_file):
            columns = [
                'timestamp', 'event_type', 'record_id', 'user_role', 
                'username', 'action', 'details', 'severity'
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.log_file, index=False)
    
    def log_event(self, event_type: str, record_id: str, user_role: str, 
                  username: str, action: str, details: str, severity: str = "INFO"):
        """
        Log an event
        
        Args:
            event_type: Type of event (TAMPER, ACCESS, MODIFY, etc.)
            record_id: Record identifier
            user_role: User role
            username: Username
            action: Action performed
            details: Additional details
            severity: Severity level (INFO, WARNING, CRITICAL)
        """
        try:
            df = pd.read_csv(self.log_file)
            
            new_log = {
                'timestamp': datetime.now().isoformat(),
                'event_type': event_type,
                'record_id': record_id,
                'user_role': user_role,
                'username': username,
                'action': action,
                'details': details,
                'severity': severity
            }
            
            new_row = pd.DataFrame([new_log])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.log_file, index=False)
        except Exception as e:
            print(f"Error logging event: {e}")
    
    def log_tamper_event(self, record_id: str, user_role: str, username: str, details: str):
        """Log a tamper detection event"""
        self.log_event(
            event_type="TAMPER",
            record_id=record_id,
            user_role=user_role,
            username=username,
            action="TAMPER_DETECTED",
            details=details,
            severity="CRITICAL"
        )
    
    def log_access(self, record_id: str, user_role: str, username: str):
        """Log a record access event"""
        self.log_event(
            event_type="ACCESS",
            record_id=record_id,
            user_role=user_role,
            username=username,
            action="VIEW_RECORD",
            details="Record accessed",
            severity="INFO"
        )
    
    def log_modification(self, record_id: str, user_role: str, username: str, details: str):
        """Log a record modification event"""
        self.log_event(
            event_type="MODIFY",
            record_id=record_id,
            user_role=user_role,
            username=username,
            action="MODIFY_RECORD",
            details=details,
            severity="WARNING"
        )
    
    def log_addition(self, record_id: str, user_role: str, username: str):
        """Log a record addition event"""
        self.log_event(
            event_type="ADD",
            record_id=record_id,
            user_role=user_role,
            username=username,
            action="ADD_RECORD",
            details="New record added",
            severity="INFO"
        )
    
    def get_all_logs(self):
        """
        Get all logs
        
        Returns:
            pandas.DataFrame: All logs
        """
        try:
            return pd.read_csv(self.log_file)
        except Exception as e:
            print(f"Error reading logs: {e}")
            return pd.DataFrame()
    
    def get_logs_by_record(self, record_id: str):
        """Get logs for a specific record"""
        try:
            df = pd.read_csv(self.log_file)
            return df[df['record_id'] == record_id]
        except Exception as e:
            print(f"Error reading logs: {e}")
            return pd.DataFrame()
    
    def get_tamper_logs(self):
        """Get all tamper detection logs"""
        try:
            df = pd.read_csv(self.log_file)
            return df[df['event_type'] == 'TAMPER']
        except Exception as e:
            print(f"Error reading logs: {e}")
            return pd.DataFrame()
    
    def get_logs_by_severity(self, severity: str):
        """Get logs by severity level"""
        try:
            df = pd.read_csv(self.log_file)
            return df[df['severity'] == severity]
        except Exception as e:
            print(f"Error reading logs: {e}")
            return pd.DataFrame()


# Global logger instance
_logger = None


def get_logger():
    """Get the global logger instance"""
    global _logger
    if _logger is None:
        _logger = Logger()
    return _logger
