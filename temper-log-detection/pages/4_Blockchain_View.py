"""
Blockchain Visualization Page
"""
import streamlit as st
from auth import get_auth_manager
from blockchain import get_blockchain
import json

st.set_page_config(page_title="Blockchain", page_icon="⛓️", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("⛓️ Blockchain Visualization")

# User info
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"👤 Logged in as: **{auth.get_current_user()}** ({auth.get_current_role()})")
with col2:
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

st.markdown("---")

# Get blockchain
blockchain = get_blockchain()

# Blockchain status
st.subheader("📊 Blockchain Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Blocks", len(blockchain.chain))

with col2:
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        st.metric("Chain Status", "✅ Valid")
    else:
        st.metric("Chain Status", "🚨 INVALID")

with col3:
    st.metric("Difficulty", blockchain.difficulty)

st.markdown("---")

# Verify blockchain button
if st.button("🔍 Verify Blockchain Integrity", use_container_width=True):
    is_valid = blockchain.is_chain_valid()
    
    if is_valid:
        st.success("✅ Blockchain integrity verified! All blocks are valid and properly linked.")
    else:
        st.error("🚨 BLOCKCHAIN COMPROMISED! Chain validation failed.")
        st.error("This indicates that the blockchain has been tampered with.")

st.markdown("---")

# Display blocks
st.subheader("🔗 Blockchain Blocks")

# Reverse order to show latest first
blocks = list(reversed(blockchain.chain))

for i, block in enumerate(blocks):
    block_dict = block.to_dict()
    
    # Determine if it's the genesis block
    is_genesis = block_dict['index'] == 0
    
    # Color coding
    if is_genesis:
        header_color = "🟢"
        block_type = "Genesis Block"
    else:
        header_color = "🔵"
        block_type = "Data Block"
    
    with st.expander(f"{header_color} Block #{block_dict['index']} - {block_type}", expanded=(i == 0)):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Block Information**")
            st.text(f"Index: {block_dict['index']}")
            st.text(f"Timestamp: {block_dict['timestamp']}")
            st.text(f"Nonce: {block_dict['nonce']}")
            
            st.markdown("**🔐 Hashes**")
            st.code(f"Block Hash:\n{block_dict['hash']}", language="text")
            st.code(f"Previous Hash:\n{block_dict['previous_hash']}", language="text")
        
        with col2:
            st.markdown("**📦 Block Data**")
            
            if is_genesis:
                st.json(block_dict['data'])
            else:
                # Display record data
                data = block_dict['data']
                st.text(f"Record ID: {data.get('record_id', 'N/A')}")
                st.text(f"Timestamp: {data.get('timestamp', 'N/A')}")
                
                st.markdown("**🔐 Record Hashes**")
                st.code(f"SHA-256:\n{data.get('sha256_hash', 'N/A')}", language="text")
                st.code(f"Quantum:\n{data.get('quantum_hash', 'N/A')}", language="text")
        
        # Verification status
        st.markdown("---")
        
        # Verify this block
        is_hash_valid = block.hash == block.calculate_hash()
        has_proof_of_work = block.hash.startswith('0' * blockchain.difficulty)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if is_hash_valid:
                st.success("✅ Hash Valid")
            else:
                st.error("❌ Hash Invalid")
        
        with col2:
            if has_proof_of_work:
                st.success("✅ Proof of Work Valid")
            else:
                st.error("❌ Proof of Work Invalid")
        
        with col3:
            if i < len(blocks) - 1:
                # Check link to previous block
                next_block = blocks[i + 1]
                is_linked = block_dict['previous_hash'] == next_block.hash
                
                if is_linked:
                    st.success("✅ Linked to Previous")
                else:
                    st.error("❌ Link Broken")
            else:
                st.info("ℹ️ Genesis Block")

st.markdown("---")

# Blockchain visualization
st.subheader("📊 Chain Visualization")

# Create a simple text-based visualization
chain_viz = ""
for block in blockchain.chain:
    chain_viz += f"Block {block.index}\n"
    chain_viz += f"Hash: {block.hash[:16]}...\n"
    chain_viz += "    ↓\n"

chain_viz += "END OF CHAIN"

st.code(chain_viz, language="text")

st.markdown("---")
st.info("💡 **Tip:** The blockchain ensures immutability. Each block contains the hash of the previous block, making it impossible to modify past records without detection.")
