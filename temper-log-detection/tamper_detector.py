"""
Tamper detection engine for real-time integrity verification
"""
from database import get_database
from logger import get_logger
from auth import get_auth_manager
from blockchain import verify_blockchain_integrity
import streamlit as st


class TamperDetector:
    """Detects and responds to tampering attempts"""
    
    def __init__(self):
        self.db = get_database()
        self.logger = get_logger()
        self.auth = get_auth_manager()
    
    def verify_record_on_access(self, record_id: str):
        """
        Verify record integrity when accessed
        
        Args:
            record_id: Record identifier
            
        Returns:
            dict: Verification results
        """
        # Log the access
        self.logger.log_access(
            record_id=record_id,
            user_role=self.auth.get_current_role() or "Unknown",
            username=self.auth.get_current_user() or "Unknown"
        )
        
        # Verify integrity
        verification = self.db.verify_record_integrity(record_id)
        
        # Check for tampering
        if verification['exists']:
            if not verification['sha256_valid'] or not verification['quantum_valid']:
                self._handle_tamper_detection(record_id, verification)
        
        return verification
    
    def verify_before_modification(self, record_id: str):
        """
        Verify record before allowing modification
        
        Args:
            record_id: Record identifier
            
        Returns:
            tuple: (is_valid, message)
        """
        verification = self.db.verify_record_integrity(record_id)
        
        if not verification['exists']:
            return False, "Record not found"
        
        if not verification['sha256_valid'] or not verification['quantum_valid']:
            self._handle_tamper_detection(record_id, verification)
            return False, "Record has been tampered with"
        
        # Check user role
        if self.auth.is_unauthorized():
            # Unauthorized user attempting modification
            self._handle_unauthorized_modification(record_id)
            return False, "Unauthorized modification attempt"
        
        return True, "Verification successful"
    
    def _handle_tamper_detection(self, record_id: str, verification: dict):
        """
        Handle detected tampering
        
        Args:
            record_id: Record identifier
            verification: Verification results
        """
        details = f"Hash mismatch detected. SHA256: {verification['sha256_valid']}, Quantum: {verification['quantum_valid']}"
        
        self.logger.log_tamper_event(
            record_id=record_id,
            user_role=self.auth.get_current_role() or "Unknown",
            username=self.auth.get_current_user() or "Unknown",
            details=details
        )
        
        # Display alert
        st.error("🚨 TAMPERING DETECTED!")
        st.error(f"Record ID: {record_id}")
        st.error(f"SHA-256 Hash Valid: {verification['sha256_valid']}")
        st.error(f"Quantum Hash Valid: {verification['quantum_valid']}")
        
        # If unauthorized user, terminate session
        if self.auth.is_unauthorized():
            self.auth.terminate_session("Tampering detected during unauthorized access")
    
    def _handle_unauthorized_modification(self, record_id: str):
        """
        Handle unauthorized modification attempt
        
        Args:
            record_id: Record identifier
        """
        details = "Unauthorized user attempted to modify record"
        
        self.logger.log_tamper_event(
            record_id=record_id,
            user_role=self.auth.get_current_role() or "Unknown",
            username=self.auth.get_current_user() or "Unknown",
            details=details
        )
        
        # Terminate session immediately
        self.auth.terminate_session("Unauthorized modification attempt detected")
    
    def log_modification(self, record_id: str, modified_fields: list):
        """
        Log a successful modification
        
        Args:
            record_id: Record identifier
            modified_fields: List of modified field names
        """
        details = f"Modified fields: {', '.join(modified_fields)}"
        
        self.logger.log_modification(
            record_id=record_id,
            user_role=self.auth.get_current_role() or "Unknown",
            username=self.auth.get_current_user() or "Unknown",
            details=details
        )
    
    def verify_blockchain(self):
        """
        Verify blockchain integrity
        
        Returns:
            bool: True if blockchain is valid
        """
        is_valid = verify_blockchain_integrity()
        
        if not is_valid:
            self.logger.log_event(
                event_type="BLOCKCHAIN",
                record_id="N/A",
                user_role=self.auth.get_current_role() or "Unknown",
                username=self.auth.get_current_user() or "Unknown",
                action="BLOCKCHAIN_VERIFICATION",
                details="Blockchain integrity check failed",
                severity="CRITICAL"
            )
        
        return is_valid
    
    def check_all_records(self):
        """
        Check integrity of all records
        
        Returns:
            dict: Summary of verification results
        """
        all_records = self.db.get_all_records()
        
        results = {
            'total': len(all_records),
            'valid': 0,
            'tampered': 0,
            'tampered_records': []
        }
        
        for record in all_records:
            verification = self.db.verify_record_integrity(record.record_id)
            
            if verification['sha256_valid'] and verification['quantum_valid']:
                results['valid'] += 1
            else:
                results['tampered'] += 1
                results['tampered_records'].append({
                    'record_id': record.record_id,
                    'patient_name': record.patient_name,
                    'sha256_valid': verification['sha256_valid'],
                    'quantum_valid': verification['quantum_valid']
                })
        
        return results


# Global tamper detector instance
_tamper_detector = None


def get_tamper_detector():
    """Get the global tamper detector instance"""
    global _tamper_detector
    if _tamper_detector is None:
        _tamper_detector = TamperDetector()
    return _tamper_detector
