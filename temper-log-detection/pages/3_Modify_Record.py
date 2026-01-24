"""
Modify Medical Record Page
"""
import streamlit as st
from auth import get_auth_manager
from database import get_database
from tamper_detector import get_tamper_detector
from models import MedicalRecord

st.set_page_config(page_title="Modify Record", page_icon="✏️", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("✏️ Modify Medical Record")

# User info
col1, col2 = st.columns([3, 1])
with col1:
    st.info(f"👤 Logged in as: **{auth.get_current_user()}** ({auth.get_current_role()})")
with col2:
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

st.markdown("---")

# Warning for unauthorized users
if auth.is_unauthorized():
    st.error("⚠️ **WARNING**: You are logged in as an Unauthorized user. Any modification attempt will trigger tamper detection and terminate your session immediately.")

# Admin warning
if auth.is_admin():
    st.warning("⚠️ **Admin Notice**: Modifications will update hashes and create new blockchain entries. All changes are logged.")

st.markdown("---")

# Get all records
db = get_database()
records = db.get_all_records()

if not records:
    st.warning("📭 No records found. Add a new record first.")
else:
    # Select record to modify
    record_options = {f"{r.patient_name} - {r.record_id}": r.record_id for r in records}
    selected_option = st.selectbox("Select Record to Modify", list(record_options.keys()))
    
    if selected_option:
        record_id = record_options[selected_option]
        
        # Verify before modification
        detector = get_tamper_detector()
        is_valid, message = detector.verify_before_modification(record_id)
        
        if not is_valid:
            st.error(f"❌ {message}")
            st.stop()
        
        # Get the record
        record = db.get_record(record_id)
        
        if record:
            st.success(f"✅ Record loaded: {record.record_id}")
            
            # Show current hashes
            with st.expander("🔐 Current Security Information"):
                col1, col2 = st.columns(2)
                with col1:
                    st.code(f"SHA-256: {record.sha256_hash}", language="text")
                with col2:
                    st.code(f"Quantum: {record.quantum_hash}", language="text")
                st.text(f"Blockchain Index: {record.blockchain_index}")
            
            st.markdown("---")
            
            # Modification form
            with st.form("modify_record_form"):
                st.subheader("📋 Section 1: Personal & Contact Information")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    patient_name = st.text_input("Patient Name *", value=record.patient_name)
                with col2:
                    age = st.text_input("Age *", value=record.age)
                with col3:
                    gender = st.selectbox("Gender *", ["Male", "Female", "Other"], 
                                        index=["Male", "Female", "Other"].index(record.gender) if record.gender in ["Male", "Female", "Other"] else 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    contact_number = st.text_input("Contact Number *", value=record.contact_number)
                with col2:
                    email = st.text_input("Email", value=record.email)
                
                address = st.text_area("Address", value=record.address)
                
                st.markdown("---")
                st.subheader("🏥 Section 2: Medical & Doctor Information")
                
                col1, col2 = st.columns(2)
                with col1:
                    doctor_name = st.text_input("Doctor Name", value=record.doctor_name)
                with col2:
                    visit_date = st.text_input("Visit Date", value=record.visit_date)
                
                diagnosis = st.text_area("Diagnosis", value=record.diagnosis)
                treatment = st.text_area("Treatment", value=record.treatment)
                medications = st.text_area("Medications", value=record.medications)
                medical_history = st.text_area("Medical History", value=record.medical_history)
                
                st.markdown("---")
                st.subheader("💰 Section 3: Billing & Payment Information")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    consultation_fee = st.text_input("Consultation Fee", value=record.consultation_fee)
                with col2:
                    medication_cost = st.text_input("Medication Cost", value=record.medication_cost)
                with col3:
                    total_amount = st.text_input("Total Amount", value=record.total_amount)
                
                col1, col2 = st.columns(2)
                with col1:
                    payment_status = st.selectbox("Payment Status", ["Paid", "Pending", "Partial"],
                                                index=["Paid", "Pending", "Partial"].index(record.payment_status) if record.payment_status in ["Paid", "Pending", "Partial"] else 0)
                with col2:
                    insurance_details = st.text_input("Insurance Details", value=record.insurance_details)
                
                st.markdown("---")
                
                # Final warning
                if auth.is_admin():
                    st.warning("⚠️ **Confirm Modification**: This will regenerate hashes and add a new block to the blockchain.")
                else:
                    st.error("🚨 **FINAL WARNING**: Proceeding will trigger tamper detection and terminate your session!")
                
                submitted = st.form_submit_button("💾 Update Record", use_container_width=True)
                
                if submitted:
                    # Track modified fields
                    modified_fields = []
                    
                    if record.patient_name != patient_name:
                        modified_fields.append("patient_name")
                        record.patient_name = patient_name
                    if record.age != age:
                        modified_fields.append("age")
                        record.age = age
                    if record.gender != gender:
                        modified_fields.append("gender")
                        record.gender = gender
                    if record.contact_number != contact_number:
                        modified_fields.append("contact_number")
                        record.contact_number = contact_number
                    if record.email != email:
                        modified_fields.append("email")
                        record.email = email
                    if record.address != address:
                        modified_fields.append("address")
                        record.address = address
                    if record.doctor_name != doctor_name:
                        modified_fields.append("doctor_name")
                        record.doctor_name = doctor_name
                    if record.visit_date != visit_date:
                        modified_fields.append("visit_date")
                        record.visit_date = visit_date
                    if record.diagnosis != diagnosis:
                        modified_fields.append("diagnosis")
                        record.diagnosis = diagnosis
                    if record.treatment != treatment:
                        modified_fields.append("treatment")
                        record.treatment = treatment
                    if record.medications != medications:
                        modified_fields.append("medications")
                        record.medications = medications
                    if record.medical_history != medical_history:
                        modified_fields.append("medical_history")
                        record.medical_history = medical_history
                    if record.consultation_fee != consultation_fee:
                        modified_fields.append("consultation_fee")
                        record.consultation_fee = consultation_fee
                    if record.medication_cost != medication_cost:
                        modified_fields.append("medication_cost")
                        record.medication_cost = medication_cost
                    if record.total_amount != total_amount:
                        modified_fields.append("total_amount")
                        record.total_amount = total_amount
                    if record.payment_status != payment_status:
                        modified_fields.append("payment_status")
                        record.payment_status = payment_status
                    if record.insurance_details != insurance_details:
                        modified_fields.append("insurance_details")
                        record.insurance_details = insurance_details
                    
                    if not modified_fields:
                        st.info("ℹ️ No changes detected.")
                    else:
                        # Update record
                        success = db.update_record(record)
                        
                        if success:
                            # Log modification
                            detector.log_modification(record_id, modified_fields)
                            
                            st.success("✅ Record updated successfully!")
                            st.success(f"📝 Modified fields: {', '.join(modified_fields)}")
                            st.success(f"🔐 New SHA-256 Hash: `{record.sha256_hash[:16]}...`")
                            st.success(f"⚛️ New Quantum Hash: `{record.quantum_hash[:16]}...`")
                            st.success(f"⛓️ New Blockchain Index: **{record.blockchain_index}**")
                            
                            st.balloons()
                        else:
                            st.error("❌ Failed to update record.")

st.markdown("---")
st.info("💡 **Tip:** All modifications are logged and create new blockchain entries. Unauthorized modifications trigger immediate detection.")
