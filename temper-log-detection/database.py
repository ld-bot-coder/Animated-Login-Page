"""
Database layer for medical records with CSV storage
"""
import pandas as pd
import os
from models import MedicalRecord
import classical_hash
import quantum_hash
from blockchain import add_record_to_blockchain
from config import CSV_FILE_PATH


class Database:
    """Database abstraction layer using CSV storage"""
    
    def __init__(self):
        self.csv_file = CSV_FILE_PATH
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create CSV file if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            # Create empty DataFrame with all columns
            columns = [
                'record_id', 'patient_name', 'age', 'gender', 'contact_number', 
                'email', 'address', 'doctor_name', 'diagnosis', 'treatment',
                'medications', 'medical_history', 'visit_date', 'consultation_fee',
                'medication_cost', 'total_amount', 'payment_status', 'insurance_details',
                'sha256_hash', 'quantum_hash', 'blockchain_index', 'timestamp'
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.csv_file, index=False)
    
    def add_record(self, record: MedicalRecord):
        """
        Add a new record to the database
        
        Args:
            record: MedicalRecord instance
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate record
            is_valid, error_msg = record.validate()
            if not is_valid:
                raise ValueError(error_msg)
            
            # Generate hashes
            data_for_hashing = record.get_data_for_hashing()
            record.sha256_hash = classical_hash.hash_record(data_for_hashing)
            record.quantum_hash = quantum_hash.hash_record(data_for_hashing)
            
            # Add to blockchain
            record.blockchain_index = add_record_to_blockchain(
                record.record_id,
                record.sha256_hash,
                record.quantum_hash
            )
            
            # Read existing data
            df = pd.read_csv(self.csv_file)
            
            # Add new record
            new_row = pd.DataFrame([record.to_dict()])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # Save to CSV
            df.to_csv(self.csv_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error adding record: {e}")
            return False
    
    def get_record(self, record_id: str):
        """
        Get a record by ID
        
        Args:
            record_id: Record identifier
            
        Returns:
            MedicalRecord or None
        """
        try:
            df = pd.read_csv(self.csv_file)
            record_data = df[df['record_id'] == record_id]
            
            if record_data.empty:
                return None
            
            # Convert to dict and create MedicalRecord
            record_dict = record_data.iloc[0].to_dict()
            return MedicalRecord.from_dict(record_dict)
        except Exception as e:
            print(f"Error getting record: {e}")
            return None
    
    def get_all_records(self):
        """
        Get all records
        
        Returns:
            list: List of MedicalRecord instances
        """
        try:
            df = pd.read_csv(self.csv_file)
            
            if df.empty:
                return []
            
            records = []
            for _, row in df.iterrows():
                record_dict = row.to_dict()
                records.append(MedicalRecord.from_dict(record_dict))
            
            return records
        except Exception as e:
            print(f"Error getting all records: {e}")
            return []
    
    def update_record(self, record: MedicalRecord):
        """
        Update an existing record
        
        Args:
            record: MedicalRecord instance with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df = pd.read_csv(self.csv_file)
            
            # Find record index
            record_index = df[df['record_id'] == record.record_id].index
            
            if record_index.empty:
                return False
            
            # Regenerate hashes with new data
            data_for_hashing = record.get_data_for_hashing()
            record.sha256_hash = classical_hash.hash_record(data_for_hashing)
            record.quantum_hash = quantum_hash.hash_record(data_for_hashing)
            
            # Add to blockchain
            record.blockchain_index = add_record_to_blockchain(
                record.record_id,
                record.sha256_hash,
                record.quantum_hash
            )
            
            # Update timestamp
            from datetime import datetime
            record.timestamp = datetime.now().isoformat()
            
            # Update the record
            for key, value in record.to_dict().items():
                df.at[record_index[0], key] = value
            
            # Save to CSV
            df.to_csv(self.csv_file, index=False)
            
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False
    
    def delete_record(self, record_id: str):
        """
        Delete a record
        
        Args:
            record_id: Record identifier
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df = pd.read_csv(self.csv_file)
            df = df[df['record_id'] != record_id]
            df.to_csv(self.csv_file, index=False)
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def verify_record_integrity(self, record_id: str):
        """
        Verify the integrity of a record by comparing hashes
        
        Args:
            record_id: Record identifier
            
        Returns:
            dict: Verification results
        """
        record = self.get_record(record_id)
        
        if not record:
            return {
                'exists': False,
                'sha256_valid': False,
                'quantum_valid': False,
                'message': 'Record not found'
            }
        
        # Get data for hashing (excluding hash fields)
        data_for_hashing = record.get_data_for_hashing()
        
        # Compute current hashes
        current_sha256 = classical_hash.hash_record(data_for_hashing)
        current_quantum = quantum_hash.hash_record(data_for_hashing)
        
        # Compare with stored hashes
        sha256_valid = (current_sha256 == record.sha256_hash)
        quantum_valid = (current_quantum == record.quantum_hash)
        
        return {
            'exists': True,
            'sha256_valid': sha256_valid,
            'quantum_valid': quantum_valid,
            'stored_sha256': record.sha256_hash,
            'computed_sha256': current_sha256,
            'stored_quantum': record.quantum_hash,
            'computed_quantum': current_quantum,
            'message': 'Integrity verified' if (sha256_valid and quantum_valid) else 'TAMPERING DETECTED!'
        }


# Global database instance
_database = None


def get_database():
    """Get the global database instance"""
    global _database
    if _database is None:
        _database = Database()
    return _database
