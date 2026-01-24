"""
Quantum-inspired hashing module using simulated quantum operations
This module simulates quantum computing concepts without requiring actual quantum hardware
"""
import numpy as np
import hashlib
import json
from config import QUANTUM_NUM_QUBITS


class QuantumHashGenerator:
    """Simulates quantum hashing using quantum gate operations"""
    
    def __init__(self, num_qubits=QUANTUM_NUM_QUBITS):
        self.num_qubits = num_qubits
        self.state_size = 2 ** num_qubits
    
    def _initialize_state(self, classical_bits):
        """
        Initialize quantum state from classical bits
        
        Args:
            classical_bits: List of 0s and 1s
            
        Returns:
            numpy.array: Quantum state vector
        """
        # Create basis state from classical bits
        state_index = int(''.join(map(str, classical_bits)), 2)
        state = np.zeros(self.state_size, dtype=complex)
        state[state_index] = 1.0
        return state
    
    def _apply_hadamard(self, state, qubit_index):
        """
        Apply Hadamard gate to create superposition
        
        Args:
            state: Current quantum state
            qubit_index: Index of qubit to apply gate to
            
        Returns:
            numpy.array: New quantum state
        """
        new_state = np.copy(state)
        step = 2 ** qubit_index
        
        for i in range(self.state_size):
            if (i // step) % 2 == 0:
                j = i + step
                if j < self.state_size:
                    temp_i = new_state[i]
                    temp_j = new_state[j]
                    new_state[i] = (temp_i + temp_j) / np.sqrt(2)
                    new_state[j] = (temp_i - temp_j) / np.sqrt(2)
        
        return new_state
    
    def _apply_phase_gate(self, state, qubit_index, phase):
        """
        Apply phase gate to introduce quantum interference
        
        Args:
            state: Current quantum state
            qubit_index: Index of qubit to apply gate to
            phase: Phase angle in radians
            
        Returns:
            numpy.array: New quantum state
        """
        new_state = np.copy(state)
        step = 2 ** qubit_index
        
        for i in range(self.state_size):
            if (i // step) % 2 == 1:
                new_state[i] *= np.exp(1j * phase)
        
        return new_state
    
    def _apply_cnot(self, state, control_qubit, target_qubit):
        """
        Apply CNOT (controlled-NOT) gate for entanglement
        
        Args:
            state: Current quantum state
            control_qubit: Control qubit index
            target_qubit: Target qubit index
            
        Returns:
            numpy.array: New quantum state
        """
        new_state = np.copy(state)
        control_step = 2 ** control_qubit
        target_step = 2 ** target_qubit
        
        for i in range(self.state_size):
            if (i // control_step) % 2 == 1:
                j = i ^ target_step
                new_state[i], new_state[j] = new_state[j], new_state[i]
        
        return new_state
    
    def _measure(self, state):
        """
        Perform measurement on quantum state
        
        Args:
            state: Quantum state to measure
            
        Returns:
            int: Measured state index
        """
        # Calculate probabilities
        probabilities = np.abs(state) ** 2
        
        # Deterministic measurement based on highest probability
        # (for consistency in hashing)
        measured_state = np.argmax(probabilities)
        
        return measured_state
    
    def _classical_to_bits(self, data_str):
        """
        Convert classical data to bit array
        
        Args:
            data_str: String data
            
        Returns:
            list: List of bits
        """
        # Use SHA-256 to get consistent bit representation
        hash_bytes = hashlib.sha256(data_str.encode('utf-8')).digest()
        
        # Convert to bits and take required number
        bits = []
        for byte in hash_bytes:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
                if len(bits) >= self.num_qubits:
                    return bits[:self.num_qubits]
        
        return bits[:self.num_qubits]
    
    def generate_quantum_hash(self, data):
        """
        Generate quantum-inspired hash for given data
        
        Args:
            data: Dictionary or string to hash
            
        Returns:
            str: Hexadecimal quantum hash
        """
        # Convert data to string
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        # Convert to classical bits
        classical_bits = self._classical_to_bits(data_str)
        
        # Initialize quantum state
        state = self._initialize_state(classical_bits)
        
        # Apply quantum gates to create complex superposition
        # Apply Hadamard gates to all qubits
        for i in range(self.num_qubits):
            state = self._apply_hadamard(state, i)
        
        # Apply phase gates with data-dependent phases
        for i in range(self.num_qubits):
            phase = (classical_bits[i] * np.pi / 4) + (i * np.pi / 8)
            state = self._apply_phase_gate(state, i, phase)
        
        # Apply CNOT gates for entanglement
        for i in range(self.num_qubits - 1):
            state = self._apply_cnot(state, i, i + 1)
        
        # Apply another round of Hadamard gates
        for i in range(self.num_qubits):
            state = self._apply_hadamard(state, i)
        
        # Measure the state
        measured_value = self._measure(state)
        
        # Convert measurement to hash
        # Combine measured value with original data for stronger hash
        combined = f"{measured_value}_{data_str}_{measured_value}"
        quantum_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        
        return quantum_hash


# Global instance
_quantum_hasher = QuantumHashGenerator()


def generate_quantum_hash(data):
    """
    Generate quantum-inspired hash for given data
    
    Args:
        data: Dictionary or string to hash
        
    Returns:
        str: Hexadecimal quantum hash
    """
    return _quantum_hasher.generate_quantum_hash(data)


def verify_quantum_hash(data, stored_hash):
    """
    Verify if data matches the stored quantum hash
    
    Args:
        data: Data to verify
        stored_hash: Previously computed quantum hash
        
    Returns:
        bool: True if hash matches, False otherwise
    """
    computed_hash = generate_quantum_hash(data)
    return computed_hash == stored_hash


def hash_record(record_dict):
    """
    Generate quantum hash for a medical record
    
    Args:
        record_dict: Dictionary containing record data
        
    Returns:
        str: Quantum hash of the record
    """
    # Create a copy without hash fields
    record_copy = {k: v for k, v in record_dict.items() 
                   if k not in ['sha256_hash', 'quantum_hash', 'blockchain_index', 'timestamp']}
    
    return generate_quantum_hash(record_copy)
