"""
Data models for medical records
"""
from datetime import datetime
from typing import Optional


class MedicalRecord:
    """Represents a medical record with three sections"""
    
    def __init__(self, record_id: str = None):
        self.record_id = record_id or self._generate_id()
        
        # Section 1: Personal and Contact Information
        self.patient_name = ""
        self.age = ""
        self.gender = ""
        self.contact_number = ""
        self.email = ""
        self.address = ""
        
        # Section 2: Medical and Doctor Information
        self.doctor_name = ""
        self.diagnosis = ""
        self.treatment = ""
        self.medications = ""
        self.medical_history = ""
        self.visit_date = ""
        
        # Section 3: Billing and Payment Information
        self.consultation_fee = ""
        self.medication_cost = ""
        self.total_amount = ""
        self.payment_status = ""
        self.insurance_details = ""
        
        # System fields
        self.sha256_hash = ""
        self.quantum_hash = ""
        self.blockchain_index = -1
        self.timestamp = datetime.now().isoformat()
    
    def _generate_id(self):
        """Generate unique record ID"""
        return f"MR{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'record_id': self.record_id,
            # Personal Information
            'patient_name': self.patient_name,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'email': self.email,
            'address': self.address,
            # Medical Information
            'doctor_name': self.doctor_name,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'medications': self.medications,
            'medical_history': self.medical_history,
            'visit_date': self.visit_date,
            # Billing Information
            'consultation_fee': self.consultation_fee,
            'medication_cost': self.medication_cost,
            'total_amount': self.total_amount,
            'payment_status': self.payment_status,
            'insurance_details': self.insurance_details,
            # System fields
            'sha256_hash': self.sha256_hash,
            'quantum_hash': self.quantum_hash,
            'blockchain_index': self.blockchain_index,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        """Create record from dictionary"""
        record = MedicalRecord(data.get('record_id'))
        
        # Personal Information
        record.patient_name = data.get('patient_name', '')
        record.age = data.get('age', '')
        record.gender = data.get('gender', '')
        record.contact_number = data.get('contact_number', '')
        record.email = data.get('email', '')
        record.address = data.get('address', '')
        
        # Medical Information
        record.doctor_name = data.get('doctor_name', '')
        record.diagnosis = data.get('diagnosis', '')
        record.treatment = data.get('treatment', '')
        record.medications = data.get('medications', '')
        record.medical_history = data.get('medical_history', '')
        record.visit_date = data.get('visit_date', '')
        
        # Billing Information
        record.consultation_fee = data.get('consultation_fee', '')
        record.medication_cost = data.get('medication_cost', '')
        record.total_amount = data.get('total_amount', '')
        record.payment_status = data.get('payment_status', '')
        record.insurance_details = data.get('insurance_details', '')
        
        # System fields
        record.sha256_hash = data.get('sha256_hash', '')
        record.quantum_hash = data.get('quantum_hash', '')
        record.blockchain_index = data.get('blockchain_index', -1)
        record.timestamp = data.get('timestamp', datetime.now().isoformat())
        
        return record
    
    def get_data_for_hashing(self):
        """Get record data excluding hash and system fields"""
        data = self.to_dict()
        # Remove fields that shouldn't be included in hash
        for field in ['sha256_hash', 'quantum_hash', 'blockchain_index', 'timestamp']:
            data.pop(field, None)
        return data
    
    def validate(self):
        """
        Validate required fields
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.patient_name:
            return False, "Patient name is required"
        if not self.age:
            return False, "Age is required"
        if not self.gender:
            return False, "Gender is required"
        if not self.contact_number:
            return False, "Contact number is required"
        
        return True, ""
