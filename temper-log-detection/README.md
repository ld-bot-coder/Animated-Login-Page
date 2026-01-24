# Quantum Hash-Based Tamper Detection System

A comprehensive security system for medical records using classical SHA-256 hashing, quantum-inspired hashing, and blockchain technology to detect unauthorized modifications and provide immutable audit trails.

## 🎯 Features

- **Dual-Hash Verification**: SHA-256 and quantum-inspired hashing for enhanced security
- **Blockchain Integration**: Custom blockchain with proof-of-work for immutable record tracking
- **Real-Time Tamper Detection**: Automatic verification on every data access
- **Role-Based Access Control**: Admin and Unauthorized user modes
- **Comprehensive Logging**: Complete audit trail of all system events
- **Interactive UI**: Streamlit-based web interface with multiple pages

## 🏗️ Architecture

### Core Components

1. **Classical Hashing** (`classical_hash.py`): SHA-256 implementation for record integrity
2. **Quantum Hashing** (`quantum_hash.py`): Simulated quantum operations using NumPy
3. **Blockchain** (`blockchain.py`): Custom blockchain with proof-of-work mining
4. **Database** (`database.py`): CSV-based storage with automatic hash generation
5. **Authentication** (`auth.py`): Session management and role-based access
6. **Tamper Detection** (`tamper_detector.py`): Real-time integrity verification
7. **Logging** (`logger.py`): Comprehensive event logging system

### Data Model

Medical records contain three sections:
- **Personal Information**: Name, age, gender, contact, email, address
- **Medical Information**: Doctor, diagnosis, treatment, medications, history, visit date
- **Billing Information**: Fees, costs, payment status, insurance

## 📋 Requirements

- Python 3.8+
- Streamlit
- NumPy
- Pandas

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/rahul/temper-log-detection
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### Login

1. Enter a username
2. Select role:
   - **Admin**: Full access with modification warnings
   - **Unauthorized**: Demonstrates tamper detection (modifications trigger session termination)

### Adding Records

1. Navigate to "Add Record" page
2. Fill in all three sections (Personal, Medical, Billing)
3. Click "Save Record"
4. System automatically generates hashes and adds to blockchain

### Viewing Records

1. Navigate to "View Records" page
2. Browse or search for records
3. Integrity is automatically verified on access
4. Use "Verify All Records" for batch verification

### Modifying Records

1. Navigate to "Modify Record" page
2. Select a record to modify
3. **Admin**: Receives warnings, modifications are logged
4. **Unauthorized**: Session terminates immediately upon modification attempt

### Blockchain Visualization

1. Navigate to "Blockchain View" page
2. View all blocks in the chain
3. Verify blockchain integrity
4. Inspect block details and linkages

### Hash Comparison

1. Navigate to "Hash Comparison" page
2. Select a record
3. Compare stored vs. computed hashes
4. Verify integrity in real-time

### Tamper Logs

1. Navigate to "Tamper Logs" page
2. Filter by event type, severity, or search term
3. View detailed event information
4. Export logs to CSV for forensic analysis

## 🔐 Security Features

### Dual Hashing

- **SHA-256**: Industry-standard cryptographic hash
- **Quantum Hash**: Simulated quantum operations for future-ready security
  - Uses Hadamard gates for superposition
  - CNOT gates for entanglement
  - Phase gates for interference
  - Deterministic measurement for consistent hashing

### Blockchain

- Proof-of-work mining (configurable difficulty)
- Each block contains previous block hash
- Tamper-evident chain structure
- Persistent storage with validation

### Tamper Detection

- Automatic verification on data access
- Hash comparison on every operation
- Immediate detection of modifications
- Session termination for unauthorized changes
- Comprehensive event logging

## 🎭 Demo Scenarios

### Scenario 1: Normal Admin Workflow

1. Login as Admin
2. Add a new medical record
3. View the record (integrity verified)
4. Modify the record (warning shown, changes logged)
5. Check blockchain and logs

### Scenario 2: Tamper Detection Demo

1. Login as Unauthorized user
2. View records (allowed)
3. Attempt to modify a record
4. Session immediately terminated
5. Event logged as CRITICAL

### Scenario 3: Hash Verification

1. Add multiple records
2. Use Hash Comparison page
3. Verify all hashes match
4. Manually corrupt data (outside app)
5. Reload and see tamper detection

## 📊 System Configuration

Edit `config.py` to customize:

- **Database**: CSV file path or MongoDB settings
- **Blockchain**: Difficulty level (number of leading zeros)
- **Quantum**: Number of simulated qubits
- **Logging**: Log file location

## 🔬 Technical Details

### Quantum-Inspired Hashing

The quantum hash uses simulated quantum computing concepts:

1. **Initialization**: Classical bits encoded into quantum state vector
2. **Superposition**: Hadamard gates create quantum superposition
3. **Entanglement**: CNOT gates entangle qubits
4. **Interference**: Phase gates introduce quantum interference
5. **Measurement**: Deterministic measurement for consistent output
6. **Finalization**: Combined with SHA-256 for final hash

### Blockchain Structure

Each block contains:
- Index
- Timestamp
- Data (record hashes)
- Previous block hash
- Nonce (proof-of-work)
- Block hash

## ⚠️ Limitations

- Quantum hash is **simulated**, not executed on real quantum hardware
- Blockchain is **local**, not distributed/decentralized
- Designed for **academic/prototype** use, not production deployment
- CSV storage is suitable for small-scale demonstrations

## 🔮 Future Enhancements

- Integration with real post-quantum cryptographic algorithms (e.g., CRYSTALS-Kyber)
- Distributed blockchain network
- Smart contracts for automated compliance
- Cloud deployment with scalability
- Support for other domains (banking, academic records, government data)
- Real quantum hardware integration (when available)

## 📁 Project Structure

```
temper-log-detection/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── classical_hash.py           # SHA-256 hashing module
├── quantum_hash.py             # Quantum-inspired hashing
├── blockchain.py               # Custom blockchain implementation
├── models.py                   # Data models
├── database.py                 # Database layer (CSV)
├── auth.py                     # Authentication & authorization
├── logger.py                   # Logging system
├── tamper_detector.py          # Tamper detection engine
├── requirements.txt            # Python dependencies
├── pages/
│   ├── 1_Add_Record.py        # Add record page
│   ├── 2_View_Records.py      # View records page
│   ├── 3_Modify_Record.py     # Modify record page
│   ├── 4_Blockchain_View.py   # Blockchain visualization
│   ├── 5_Hash_Comparison.py   # Hash comparison page
│   └── 6_Tamper_Logs.py       # Tamper logs page
└── data/                       # Auto-created data directory
    ├── medical_records.csv     # Records database
    ├── blockchain.json         # Blockchain storage
    └── tamper_logs.csv         # Event logs
```

## 🎓 Academic Context

This project demonstrates:
- Cryptographic hash functions
- Quantum computing concepts (simulated)
- Blockchain technology
- Security principles (integrity, immutability, auditability)
- Access control mechanisms
- Forensic logging

Suitable for:
- Computer Science projects
- Cybersecurity demonstrations
- Blockchain education
- Quantum computing introduction
- Healthcare IT security

## 📝 License

This is an academic/educational project. Use at your own discretion.

## 👨‍💻 Developer Notes

- All hashes are deterministic (same input = same output)
- Blockchain mining may take a few seconds depending on difficulty
- Session state is managed by Streamlit
- Data persists in CSV files between sessions
- Logs accumulate over time (consider periodic cleanup)

## 🆘 Troubleshooting

**Issue**: Streamlit won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Data directory errors
- **Solution**: The `data/` directory is auto-created. Ensure write permissions.

**Issue**: Blockchain validation fails
- **Solution**: Delete `data/blockchain.json` to reset the chain

**Issue**: Hash mismatches on valid records
- **Solution**: Ensure no manual CSV edits. Use only the application interface.

## 📞 Support

For issues or questions about this academic project, please refer to the code comments and this documentation.

---

**Built with ❤️ for secure medical record management**
