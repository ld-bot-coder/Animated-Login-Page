"""
Classical SHA-256 hashing module for record integrity verification
"""
import hashlib
import json


def generate_sha256_hash(data):
    """
    Generate SHA-256 hash for given data
    
    Args:
        data: Dictionary or string to hash
        
    Returns:
        str: Hexadecimal SHA-256 hash
    """
    if isinstance(data, dict):
        # Convert dict to sorted JSON string for consistent hashing
        data_str = json.dumps(data, sort_keys=True)
    else:
        data_str = str(data)
    
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()


def verify_hash(data, stored_hash):
    """
    Verify if data matches the stored hash
    
    Args:
        data: Data to verify
        stored_hash: Previously computed hash
        
    Returns:
        bool: True if hash matches, False otherwise
    """
    computed_hash = generate_sha256_hash(data)
    return computed_hash == stored_hash


def hash_record(record_dict):
    """
    Generate SHA-256 hash for a medical record
    
    Args:
        record_dict: Dictionary containing record data
        
    Returns:
        str: SHA-256 hash of the record
    """
    # Create a copy without hash fields to avoid circular hashing
    record_copy = {k: v for k, v in record_dict.items() 
                   if k not in ['sha256_hash', 'quantum_hash', 'blockchain_index', 'timestamp']}
    
    return generate_sha256_hash(record_copy)


def compare_hashes(hash1, hash2):
    """
    Compare two hashes for equality
    
    Args:
        hash1: First hash
        hash2: Second hash
        
    Returns:
        bool: True if hashes match, False otherwise
    """
    return hash1 == hash2
