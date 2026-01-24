"""
Custom blockchain implementation for immutable record tracking
"""
import json
import hashlib
from datetime import datetime
from config import BLOCKCHAIN_FILE, BLOCKCHAIN_DIFFICULTY


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Contains record hashes
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate the hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine the block using proof-of-work
        
        Args:
            difficulty: Number of leading zeros required
        """
        target = '0' * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @staticmethod
    def from_dict(block_dict):
        """Create block from dictionary"""
        block = Block(
            block_dict['index'],
            block_dict['timestamp'],
            block_dict['data'],
            block_dict['previous_hash'],
            block_dict['nonce']
        )
        block.hash = block_dict['hash']
        return block


class Blockchain:
    """Manages the blockchain"""
    
    def __init__(self, difficulty=BLOCKCHAIN_DIFFICULTY):
        self.chain = []
        self.difficulty = difficulty
        self.load_blockchain()
        
        # Create genesis block if chain is empty
        if len(self.chain) == 0:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.now().isoformat(), 
                             {"message": "Genesis Block"}, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_blockchain()
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1] if self.chain else None
    
    def add_block(self, data):
        """
        Add a new block to the chain
        
        Args:
            data: Data to store in the block (record hashes)
            
        Returns:
            Block: The newly added block
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            datetime.now().isoformat(),
            data,
            latest_block.hash if latest_block else "0"
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_blockchain()
        
        return new_block
    
    def is_chain_valid(self):
        """
        Validate the entire blockchain
        
        Returns:
            bool: True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof of work
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        
        return True
    
    def save_blockchain(self):
        """Save blockchain to file"""
        try:
            with open(BLOCKCHAIN_FILE, 'w') as f:
                chain_data = [block.to_dict() for block in self.chain]
                json.dump(chain_data, f, indent=2)
        except Exception as e:
            print(f"Error saving blockchain: {e}")
    
    def load_blockchain(self):
        """Load blockchain from file"""
        try:
            with open(BLOCKCHAIN_FILE, 'r') as f:
                chain_data = json.load(f)
                self.chain = [Block.from_dict(block_dict) for block_dict in chain_data]
        except FileNotFoundError:
            # File doesn't exist yet, will create genesis block
            pass
        except Exception as e:
            print(f"Error loading blockchain: {e}")
    
    def get_block_by_index(self, index):
        """
        Get block by its index
        
        Args:
            index: Block index
            
        Returns:
            Block or None
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_all_blocks(self):
        """Get all blocks in the chain"""
        return [block.to_dict() for block in self.chain]


# Global blockchain instance
_blockchain = None


def get_blockchain():
    """Get the global blockchain instance"""
    global _blockchain
    if _blockchain is None:
        _blockchain = Blockchain()
    return _blockchain


def add_record_to_blockchain(record_id, sha256_hash, quantum_hash):
    """
    Add a record's hashes to the blockchain
    
    Args:
        record_id: Unique record identifier
        sha256_hash: SHA-256 hash of the record
        quantum_hash: Quantum hash of the record
        
    Returns:
        int: Index of the block in the blockchain
    """
    blockchain = get_blockchain()
    
    block_data = {
        'record_id': record_id,
        'sha256_hash': sha256_hash,
        'quantum_hash': quantum_hash,
        'timestamp': datetime.now().isoformat()
    }
    
    block = blockchain.add_block(block_data)
    return block.index


def verify_blockchain_integrity():
    """
    Verify the integrity of the blockchain
    
    Returns:
        bool: True if blockchain is valid, False otherwise
    """
    blockchain = get_blockchain()
    return blockchain.is_chain_valid()


def get_blockchain_status():
    """
    Get blockchain status information
    
    Returns:
        dict: Blockchain status
    """
    blockchain = get_blockchain()
    return {
        'total_blocks': len(blockchain.chain),
        'is_valid': blockchain.is_chain_valid(),
        'latest_block_hash': blockchain.get_latest_block().hash if blockchain.get_latest_block() else None
    }
