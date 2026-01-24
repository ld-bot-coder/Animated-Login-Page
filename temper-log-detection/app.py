"""
Quantum Hash-Based Tamper Detection System
Main Streamlit Application
"""
import streamlit as st
from auth import get_auth_manager
from config import ROLE_ADMIN, ROLE_UNAUTHORIZED
from blockchain import get_blockchain_status

# Page configuration
st.set_page_config(
    page_title="Quantum Tamper Detection System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize auth manager
auth = get_auth_manager()


def show_login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">🔒 Quantum Tamper Detection System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🔐 Secure Medical Record Management</h3>
        <p>This system uses quantum-inspired hashing and blockchain technology to detect 
        unauthorized modifications in medical records.</p>
        <ul>
            <li>✅ Dual-hash verification (SHA-256 + Quantum)</li>
            <li>✅ Blockchain-based immutability</li>
            <li>✅ Real-time tamper detection</li>
            <li>✅ Comprehensive audit logging</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔑 Login")
        
        username = st.text_input("Username", placeholder="Enter your username")
        
        role = st.selectbox(
            "Select Role",
            [ROLE_ADMIN, ROLE_UNAUTHORIZED],
            help="Admin: Full access with warnings. Unauthorized: Demonstration of tamper detection."
        )
        
        if role == ROLE_UNAUTHORIZED:
            st.warning("⚠️ **Demo Mode**: Selecting 'Unauthorized' will demonstrate tamper detection. Any modification attempt will trigger immediate session termination.")
        
        if st.button("🚀 Login", use_container_width=True):
            if username:
                if auth.login(username, role):
                    st.success(f"✅ Logged in as {username} ({role})")
                    st.rerun()
            else:
                st.error("Please enter a username")


def show_dashboard():
    """Display main dashboard"""
    st.markdown('<h1 class="main-header">🔒 Quantum Tamper Detection Dashboard</h1>', unsafe_allow_html=True)
    
    # User info
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.info(f"👤 **User:** {auth.get_current_user()}")
    with col2:
        role = auth.get_current_role()
        if role == ROLE_ADMIN:
            st.success(f"🔑 **Role:** {role}")
        else:
            st.warning(f"⚠️ **Role:** {role}")
    with col3:
        if st.button("🚪 Logout"):
            auth.logout()
            st.rerun()
    
    st.markdown("---")
    
    # System status
    st.subheader("📊 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        from database import get_database
        db = get_database()
        records = db.get_all_records()
        st.metric("📁 Total Records", len(records))
    
    with col2:
        blockchain_status = get_blockchain_status()
        st.metric("⛓️ Blockchain Blocks", blockchain_status['total_blocks'])
    
    with col3:
        is_valid = blockchain_status['is_valid']
        if is_valid:
            st.metric("✅ Blockchain Status", "Valid")
        else:
            st.metric("🚨 Blockchain Status", "INVALID")
    
    st.markdown("---")
    
    # Features
    st.subheader("🎯 Available Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>📝 Record Management</h4>
            <ul>
                <li>Add new medical records</li>
                <li>View existing records</li>
                <li>Modify records (with tamper detection)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>🔍 Verification Tools</h4>
            <ul>
                <li>Hash comparison and verification</li>
                <li>Blockchain integrity check</li>
                <li>Real-time tamper detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>⛓️ Blockchain</h4>
            <ul>
                <li>View complete blockchain</li>
                <li>Verify chain integrity</li>
                <li>Track record history</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h4>📋 Audit Logs</h4>
            <ul>
                <li>View tamper events</li>
                <li>Track user actions</li>
                <li>Export forensic data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instructions
    st.subheader("📖 Quick Start Guide")
    
    if auth.is_admin():
        st.markdown("""
        <div class="success-box">
            <h4>👨‍💼 Admin Mode</h4>
            <ol>
                <li>Use the sidebar to navigate between pages</li>
                <li>Add new records using the "Add Record" page</li>
                <li>View and verify records in "View Records"</li>
                <li>Modifications will show warnings but are allowed</li>
                <li>Check tamper logs to see all system events</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Unauthorized Mode (Demo)</h4>
            <ol>
                <li>You can view records and blockchain data</li>
                <li>Any attempt to modify records will be detected</li>
                <li>Session will be terminated immediately upon modification attempt</li>
                <li>All actions are logged for audit purposes</li>
            </ol>
            <p><strong>Note:</strong> This mode demonstrates the tamper detection capabilities of the system.</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application logic"""
    
    # Check authentication
    if not auth.is_authenticated():
        show_login_page()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
