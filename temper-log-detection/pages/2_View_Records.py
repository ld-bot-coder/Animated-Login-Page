"""
View Medical Records Page
"""
import streamlit as st
from auth import get_auth_manager
from database import get_database
from tamper_detector import get_tamper_detector
import pandas as pd

st.set_page_config(page_title="View Records", page_icon="👁️", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("👁️ View Medical Records")

# User info
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"👤 Logged in as: **{auth.get_current_user()}** ({auth.get_current_role()})")
with col2:
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

st.markdown("---")

# Get all records
db = get_database()
records = db.get_all_records()

if not records:
    st.warning("📭 No records found. Add a new record to get started.")
else:
    st.success(f"📊 Total Records: **{len(records)}**")
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search", placeholder="Search by patient name, record ID, or doctor name")
    with col2:
        verify_all = st.button("🔐 Verify All Records", use_container_width=True)
    
    # Filter records
    filtered_records = records
    if search_term:
        filtered_records = [
            r for r in records 
            if search_term.lower() in r.patient_name.lower() 
            or search_term.lower() in r.record_id.lower()
            or search_term.lower() in r.doctor_name.lower()
        ]
    
    if verify_all:
        st.subheader("🔍 Verification Results")
        detector = get_tamper_detector()
        results = detector.check_all_records()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", results['total'])
        with col2:
            st.metric("✅ Valid", results['valid'])
        with col3:
            st.metric("🚨 Tampered", results['tampered'])
        
        if results['tampered'] > 0:
            st.error("🚨 Tampered Records Detected!")
            for tampered in results['tampered_records']:
                st.error(f"Record ID: {tampered['record_id']} - {tampered['patient_name']}")
        else:
            st.success("✅ All records are valid!")
        
        st.markdown("---")
    
    # Display records
    st.subheader(f"📋 Records ({len(filtered_records)})")
    
    for record in filtered_records:
        with st.expander(f"📄 {record.patient_name} - {record.record_id}"):
            # Verify integrity on access
            detector = get_tamper_detector()
            verification = detector.verify_record_on_access(record.record_id)
            
            # Show integrity status
            if verification['sha256_valid'] and verification['quantum_valid']:
                st.success("✅ Record integrity verified")
            else:
                st.error("🚨 TAMPERING DETECTED!")
                st.error(f"SHA-256 Valid: {verification['sha256_valid']}")
                st.error(f"Quantum Hash Valid: {verification['quantum_valid']}")
            
            # Display record details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📋 Personal Information**")
                st.text(f"Name: {record.patient_name}")
                st.text(f"Age: {record.age}")
                st.text(f"Gender: {record.gender}")
                st.text(f"Contact: {record.contact_number}")
                st.text(f"Email: {record.email}")
                st.text(f"Address: {record.address}")
            
            with col2:
                st.markdown("**🏥 Medical Information**")
                st.text(f"Doctor: {record.doctor_name}")
                st.text(f"Visit Date: {record.visit_date}")
                st.text(f"Diagnosis: {record.diagnosis}")
                st.text(f"Treatment: {record.treatment}")
                st.text(f"Medications: {record.medications}")
                st.text(f"History: {record.medical_history}")
            
            with col3:
                st.markdown("**💰 Billing Information**")
                st.text(f"Consultation: {record.consultation_fee}")
                st.text(f"Medication: {record.medication_cost}")
                st.text(f"Total: {record.total_amount}")
                st.text(f"Status: {record.payment_status}")
                st.text(f"Insurance: {record.insurance_details}")
            
            st.markdown("---")
            
            # Hash information
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔐 Security Information**")
                st.code(f"SHA-256: {record.sha256_hash}", language="text")
                st.code(f"Quantum: {record.quantum_hash}", language="text")
            
            with col2:
                st.markdown("**⛓️ Blockchain Information**")
                st.text(f"Block Index: {record.blockchain_index}")
                st.text(f"Timestamp: {record.timestamp}")

st.markdown("---")
st.info("💡 **Tip:** Record integrity is automatically verified when you view it. Any tampering will be immediately detected and logged.")
