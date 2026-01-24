"""
Configuration settings for the Quantum Hash-Based Tamper Detection System
"""
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database settings
DATABASE_TYPE = "CSV"  # Options: "CSV" or "MONGODB"
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "medical_records.csv")
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DB_NAME = "tamper_detection"
MONGODB_COLLECTION = "medical_records"

# Blockchain settings
BLOCKCHAIN_FILE = os.path.join(BASE_DIR, "data", "blockchain.json")
BLOCKCHAIN_DIFFICULTY = 4  # Number of leading zeros required in hash

# Logging settings
TAMPER_LOG_FILE = os.path.join(BASE_DIR, "data", "tamper_logs.csv")

# Quantum hash settings
QUANTUM_NUM_QUBITS = 8  # Number of simulated qubits for quantum hashing

# Security settings
SESSION_TIMEOUT = 3600  # Session timeout in seconds

# User roles
ROLE_ADMIN = "Admin"
ROLE_UNAUTHORIZED = "Unauthorized"

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
