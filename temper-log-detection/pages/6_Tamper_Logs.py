"""
Tamper Logs Page
"""
import streamlit as st
from auth import get_auth_manager
from logger import get_logger
import pandas as pd

st.set_page_config(page_title="Tamper Logs", page_icon="📋", layout="wide")

auth = get_auth_manager()
auth.require_auth()

st.title("📋 Tamper Detection Logs")

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
This page displays all system events including tamper detection, record access, modifications, and additions.
Use the filters below to narrow down the logs.
""")

st.markdown("---")

# Get logger
logger = get_logger()

# Filter options
col1, col2, col3 = st.columns(3)

with col1:
    event_filter = st.selectbox(
        "Event Type",
        ["All", "TAMPER", "ACCESS", "MODIFY", "ADD", "BLOCKCHAIN"]
    )

with col2:
    severity_filter = st.selectbox(
        "Severity",
        ["All", "CRITICAL", "WARNING", "INFO"]
    )

with col3:
    search_term = st.text_input("Search", placeholder="Record ID or username")

# Get all logs
all_logs = logger.get_all_logs()

if all_logs.empty:
    st.info("📭 No logs found. System events will appear here.")
else:
    # Apply filters
    filtered_logs = all_logs.copy()
    
    if event_filter != "All":
        filtered_logs = filtered_logs[filtered_logs['event_type'] == event_filter]
    
    if severity_filter != "All":
        filtered_logs = filtered_logs[filtered_logs['severity'] == severity_filter]
    
    if search_term:
        filtered_logs = filtered_logs[
            filtered_logs['record_id'].str.contains(search_term, case=False, na=False) |
            filtered_logs['username'].str.contains(search_term, case=False, na=False)
        ]
    
    # Display summary
    st.subheader("📊 Log Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Events", len(all_logs))
    
    with col2:
        tamper_count = len(all_logs[all_logs['event_type'] == 'TAMPER'])
        st.metric("🚨 Tamper Events", tamper_count)
    
    with col3:
        critical_count = len(all_logs[all_logs['severity'] == 'CRITICAL'])
        st.metric("⚠️ Critical Events", critical_count)
    
    with col4:
        st.metric("Filtered Results", len(filtered_logs))
    
    st.markdown("---")
    
    # Display logs
    st.subheader(f"📝 Event Logs ({len(filtered_logs)})")
    
    if filtered_logs.empty:
        st.info("No logs match the current filters.")
    else:
        # Sort by timestamp (most recent first)
        filtered_logs = filtered_logs.sort_values('timestamp', ascending=False)
        
        # Display each log entry
        for idx, log in filtered_logs.iterrows():
            # Determine color based on severity
            if log['severity'] == 'CRITICAL':
                severity_color = "🔴"
                box_class = "danger-box"
            elif log['severity'] == 'WARNING':
                severity_color = "🟡"
                box_class = "warning-box"
            else:
                severity_color = "🟢"
                box_class = "info-box"
            
            # Event type icon
            event_icons = {
                'TAMPER': '🚨',
                'ACCESS': '👁️',
                'MODIFY': '✏️',
                'ADD': '➕',
                'BLOCKCHAIN': '⛓️'
            }
            event_icon = event_icons.get(log['event_type'], '📝')
            
            with st.expander(
                f"{severity_color} {event_icon} {log['event_type']} - {log['record_id']} - {log['timestamp']}"
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📋 Event Information**")
                    st.text(f"Event Type: {log['event_type']}")
                    st.text(f"Severity: {log['severity']}")
                    st.text(f"Timestamp: {log['timestamp']}")
                    st.text(f"Action: {log['action']}")
                
                with col2:
                    st.markdown("**👤 User Information**")
                    st.text(f"Username: {log['username']}")
                    st.text(f"Role: {log['user_role']}")
                    st.text(f"Record ID: {log['record_id']}")
                
                st.markdown("**📝 Details**")
                st.text(log['details'])
                
                # Highlight critical events
                if log['severity'] == 'CRITICAL':
                    st.error("⚠️ This is a critical security event!")
    
    st.markdown("---")
    
    # Export logs
    st.subheader("💾 Export Logs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Filtered Logs (CSV)", use_container_width=True):
            csv = filtered_logs.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="tamper_logs.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Download All Logs (CSV)", use_container_width=True):
            csv = all_logs.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="all_logs.csv",
                mime="text/csv"
            )
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📈 Event Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Events by Type**")
        event_counts = all_logs['event_type'].value_counts()
        st.bar_chart(event_counts)
    
    with col2:
        st.markdown("**Events by Severity**")
        severity_counts = all_logs['severity'].value_counts()
        st.bar_chart(severity_counts)

st.markdown("---")
st.info("💡 **Tip:** All system events are logged with timestamps and user information for complete audit trails. Critical events indicate potential security breaches.")
