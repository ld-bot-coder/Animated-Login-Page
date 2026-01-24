"""
Hash Comparison Page
"""
import streamlit as st
from auth import get_auth_manager
from database import get_database
import classical_hash
import quantum_hash

st.set_page_config(page_title="Hash Comparison", page_icon="🔍", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("🔍 Hash Comparison & Verification")

# User info
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"👤 Logged in as: **{auth.get_current_user()}** ({auth.get_current_role()})")
with col2:
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

st.markdown("---")

st.markdown("""
This page allows you to compare stored hashes with freshly computed hashes to verify record integrity.
Any mismatch indicates that the record has been tampered with.
""")

st.markdown("---")

# Get all records
db = get_database()
records = db.get_all_records()

if not records:
    st.warning("📭 No records found. Add a new record first.")
else:
    # Select record
    record_options = {f"{r.patient_name} - {r.record_id}": r.record_id for r in records}
    selected_option = st.selectbox("Select Record to Verify", list(record_options.keys()))
    
    if selected_option:
        record_id = record_options[selected_option]
        
        # Get verification results
        verification = db.verify_record_integrity(record_id)
        
        if verification['exists']:
            record = db.get_record(record_id)
            
            # Overall status
            st.subheader("📊 Verification Status")
            
            if verification['sha256_valid'] and verification['quantum_valid']:
                st.success("✅ **RECORD INTEGRITY VERIFIED**")
                st.success("Both SHA-256 and Quantum hashes match. No tampering detected.")
            else:
                st.error("🚨 **TAMPERING DETECTED!**")
                st.error("Hash mismatch indicates unauthorized modification.")
            
            st.markdown("---")
            
            # SHA-256 Comparison
            st.subheader("🔐 SHA-256 Hash Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📦 Stored Hash**")
                st.code(verification['stored_sha256'], language="text")
            
            with col2:
                st.markdown("**🔄 Computed Hash**")
                st.code(verification['computed_sha256'], language="text")
            
            if verification['sha256_valid']:
                st.success("✅ SHA-256 hashes match")
            else:
                st.error("❌ SHA-256 hashes DO NOT match - TAMPERING DETECTED!")
            
            st.markdown("---")
            
            # Quantum Hash Comparison
            st.subheader("⚛️ Quantum Hash Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📦 Stored Hash**")
                st.code(verification['stored_quantum'], language="text")
            
            with col2:
                st.markdown("**🔄 Computed Hash**")
                st.code(verification['computed_quantum'], language="text")
            
            if verification['quantum_valid']:
                st.success("✅ Quantum hashes match")
            else:
                st.error("❌ Quantum hashes DO NOT match - TAMPERING DETECTED!")
            
            st.markdown("---")
            
            # Record details
            st.subheader("📋 Record Details")
            
            with st.expander("View Record Data"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Personal Information**")
                    st.json({
                        "patient_name": record.patient_name,
                        "age": record.age,
                        "gender": record.gender,
                        "contact_number": record.contact_number,
                        "email": record.email,
                        "address": record.address
                    })
                
                with col2:
                    st.markdown("**Medical Information**")
                    st.json({
                        "doctor_name": record.doctor_name,
                        "diagnosis": record.diagnosis,
                        "treatment": record.treatment,
                        "medications": record.medications,
                        "medical_history": record.medical_history,
                        "visit_date": record.visit_date
                    })
                
                with col3:
                    st.markdown("**Billing Information**")
                    st.json({
                        "consultation_fee": record.consultation_fee,
                        "medication_cost": record.medication_cost,
                        "total_amount": record.total_amount,
                        "payment_status": record.payment_status,
                        "insurance_details": record.insurance_details
                    })
            
            st.markdown("---")
            
            # Blockchain information
            st.subheader("⛓️ Blockchain Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Blockchain Index", record.blockchain_index)
            
            with col2:
                st.metric("Last Updated", record.timestamp)
        else:
            st.error("❌ Record not found")

st.markdown("---")

# Batch verification
st.subheader("🔍 Batch Verification")

if st.button("Verify All Records", use_container_width=True):
    st.markdown("### Verification Results")
    
    all_valid = True
    
    for record in records:
        verification = db.verify_record_integrity(record.record_id)
        
        if verification['sha256_valid'] and verification['quantum_valid']:
            st.success(f"✅ {record.patient_name} ({record.record_id}) - Valid")
        else:
            st.error(f"🚨 {record.patient_name} ({record.record_id}) - TAMPERED!")
            all_valid = False
    
    st.markdown("---")
    
    if all_valid:
        st.success("🎉 All records verified successfully!")
    else:
        st.error("⚠️ Some records have been tampered with!")

st.markdown("---")
st.info("💡 **Tip:** Hash comparison is performed in real-time. Any modification to the record data will result in different hash values, immediately revealing tampering.")
