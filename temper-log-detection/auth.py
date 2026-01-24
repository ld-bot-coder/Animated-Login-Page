"""
Authentication and authorization module
"""
import streamlit as st
from config import ROLE_ADMIN, ROLE_UNAUTHORIZED


class AuthManager:
    """Manages user authentication and authorization"""
    
    def __init__(self):
        self._initialize_session()
    
    def _initialize_session(self):
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'username' not in st.session_state:
            st.session_state.username = None
    
    def login(self, username: str, role: str):
        """
        Log in a user
        
        Args:
            username: Username
            role: User role (Admin or Unauthorized)
            
        Returns:
            bool: True if login successful
        """
        if not username:
            return False
        
        st.session_state.authenticated = True
        st.session_state.user_role = role
        st.session_state.username = username
        
        return True
    
    def logout(self):
        """Log out the current user"""
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Get current username"""
        return st.session_state.get('username', None)
    
    def get_current_role(self):
        """Get current user role"""
        return st.session_state.get('user_role', None)
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.get_current_role() == ROLE_ADMIN
    
    def is_unauthorized(self):
        """Check if current user is unauthorized"""
        return self.get_current_role() == ROLE_UNAUTHORIZED
    
    def require_auth(self):
        """
        Require authentication to proceed
        Redirects to login if not authenticated
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        if not self.is_authenticated():
            st.warning("⚠️ Please log in to access this page")
            st.stop()
            return False
        return True
    
    def terminate_session(self, reason: str = "Unauthorized action detected"):
        """
        Terminate the current session
        
        Args:
            reason: Reason for termination
        """
        st.error(f"🚨 SESSION TERMINATED: {reason}")
        self.logout()
        st.stop()


# Global auth manager instance
_auth_manager = None


def get_auth_manager():
    """Get the global auth manager instance"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
