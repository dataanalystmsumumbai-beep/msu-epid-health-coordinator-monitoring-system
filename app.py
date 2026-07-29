import streamlit as st

from core.session import (
    initialize_session,
    login
)

from services.auth_service import AuthService
from utils.security import verify_password

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="MSU/EPID Health Coordinator Monitoring System",
    page_icon="🏥",
    layout="wide"
)

initialize_session()

# -----------------------------
# Login Screen
# -----------------------------

if not st.session_state.logged_in:

    st.title("🏥 MSU/EPID Health Coordinator Monitoring System")

    st.subheader("Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    login_button = st.button(
        "Login",
        use_container_width=True
    )

    if login_button:

        user = AuthService.get_user(username)

        if user is None:

            st.error("Invalid Username")

            st.stop()

        if str(user["Status"]).upper() != "ACTIVE":

            st.error("Account Disabled")

            st.stop()

        if not verify_password(
            password,
            user["Password_Hash"]
        ):

            st.error("Invalid Password")

            st.stop()

        login(user)

        st.rerun()

# -----------------------------
# Dashboard Redirect
# -----------------------------

role = st.session_state.role

st.success(
    f"Welcome {st.session_state.full_name}"
)

if role == "Developer":

    st.switch_page(
        "pages/00_Developer_Dashboard.py"
    )

elif role == "Admin":

    st.switch_page(
        "pages/01_Admin_Dashboard.py"
    )

elif role == "Coordinator":

    st.switch_page(
        "pages/02_Coordinator_Dashboard.py"
    )
