import streamlit as st

from core.navigation import redirect_after_login

from core.session import (
    initialize_session,
    login
)

from services.auth_service import AuthService

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

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
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

            st.stop()

# -----------------------------
# Redirect
# -----------------------------

if st.session_state.logged_in:
    redirect_after_login()
