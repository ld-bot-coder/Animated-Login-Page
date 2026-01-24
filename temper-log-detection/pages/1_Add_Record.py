"""
Add Medical Record Page
"""
import streamlit as st
from auth import get_auth_manager
from database import get_database
from models import MedicalRecord
from logger import get_logger
from datetime import date

st.set_page_config(page_title="Add Record", page_icon="➕", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("➕ Add New Medical Record")

# User info
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"👤 Logged in as: **{auth.get_current_user()}** ({auth.get_current_role()})")
with col2:
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

st.markdown("---")

# Create form
with st.form("add_record_form"):
    st.subheader("📋 Section 1: Personal & Contact Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        patient_name = st.text_input("Patient Name *", placeholder="Full name")
    with col2:
        age = st.text_input("Age *", placeholder="Age in years")
    with col3:
        gender = st.selectbox("Gender *", ["", "Male", "Female", "Other"])
    
    col1, col2 = st.columns(2)
    with col1:
        contact_number = st.text_input("Contact Number *", placeholder="+1234567890")
    with col2:
        email = st.text_input("Email", placeholder="patient@example.com")
    
    address = st.text_area("Address", placeholder="Full address")
    
    st.markdown("---")
    st.subheader("🏥 Section 2: Medical & Doctor Information")
    
    col1, col2 = st.columns(2)
    with col1:
        doctor_name = st.text_input("Doctor Name", placeholder="Dr. Name")
    with col2:
        visit_date = st.date_input("Visit Date", value=date.today())
    
    diagnosis = st.text_area("Diagnosis", placeholder="Medical diagnosis")
    treatment = st.text_area("Treatment", placeholder="Prescribed treatment")
    medications = st.text_area("Medications", placeholder="List of medications")
    medical_history = st.text_area("Medical History", placeholder="Previous medical conditions")
    
    st.markdown("---")
    st.subheader("💰 Section 3: Billing & Payment Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        consultation_fee = st.text_input("Consultation Fee", placeholder="0.00")
    with col2:
        medication_cost = st.text_input("Medication Cost", placeholder="0.00")
    with col3:
        total_amount = st.text_input("Total Amount", placeholder="0.00")
    
    col1, col2 = st.columns(2)
    with col1:
        payment_status = st.selectbox("Payment Status", ["", "Paid", "Pending", "Partial"])
    with col2:
        insurance_details = st.text_input("Insurance Details", placeholder="Insurance provider and policy number")
    
    st.markdown("---")
    
    submitted = st.form_submit_button("💾 Save Record", use_container_width=True)

# Handle form submission outside the form
if submitted:
    # Create record
    record = MedicalRecord()
    
    # Personal information
    record.patient_name = patient_name
    record.age = age
    record.gender = gender
    record.contact_number = contact_number
    record.email = email
    record.address = address
    
    # Medical information
    record.doctor_name = doctor_name
    record.diagnosis = diagnosis
    record.treatment = treatment
    record.medications = medications
    record.medical_history = medical_history
    record.visit_date = str(visit_date)
    
    # Billing information
    record.consultation_fee = consultation_fee
    record.medication_cost = medication_cost
    record.total_amount = total_amount
    record.payment_status = payment_status
    record.insurance_details = insurance_details
    
    # Validate
    is_valid, error_msg = record.validate()
    
    if not is_valid:
        st.error(f"❌ Validation Error: {error_msg}")
    else:
        # Save to database
        db = get_database()
        success = db.add_record(record)
        
        if success:
            # Log the addition
            logger = get_logger()
            logger.log_addition(
                record_id=record.record_id,
                user_role=auth.get_current_role(),
                username=auth.get_current_user()
            )
            
            st.success(f"✅ Record saved successfully!")
            st.success(f"📝 Record ID: **{record.record_id}**")
            st.success(f"🔐 SHA-256 Hash: `{record.sha256_hash[:16]}...`")
            st.success(f"⚛️ Quantum Hash: `{record.quantum_hash[:16]}...`")
            st.success(f"⛓️ Blockchain Index: **{record.blockchain_index}**")
            st.info("💡 Scroll up to add another record or use the sidebar to navigate to other pages.")
            
            st.balloons()
        else:
            st.error("❌ Failed to save record. Please try again.")

st.markdown("---")
st.info("💡 **Tip:** Fields marked with * are required. All data is automatically hashed and added to the blockchain upon saving.")
