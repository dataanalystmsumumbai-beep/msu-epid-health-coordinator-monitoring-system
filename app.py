import streamlit as st

from core.session import (
    initialize_session,
    login
)

from core.navigation import redirect_after_login
from services.auth_service import AuthService

# ======================================================
# Page Configuration
# ======================================================

st.set_page_config(
    page_title="MSU / EPID Health Coordinator Monitoring System",
    page_icon="🏥",
    layout="wide"
)

# ======================================================
# Initialize Session
# ======================================================

initialize_session()

# ======================================================
# Redirect if Already Logged In
# ======================================================

if st.session_state.get("logged_in", False):
    redirect_after_login()

# ======================================================
# Login Screen
# ======================================================

st.title("🏥 MSU / EPID Health Coordinator Monitoring System")
st.subheader("Secure Login")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button(
    "🔐 Login",
    use_container_width=True
):

    status, result = AuthService.authenticate(
        username,
        password
    )

    if status:

        login(result)

        st.success("Login Successful")

        st.rerun()

    else:

        st.error(result)
