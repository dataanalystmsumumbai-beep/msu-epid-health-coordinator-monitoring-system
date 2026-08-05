import streamlit as st

from core.navigation import redirect_after_login
from core.session import initialize_session, login
from services.auth_service import AuthService

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="MSU/EPID Health Coordinator Monitoring System",
    page_icon="🏥",
    layout="wide"
)

initialize_session()

# ==========================================================
# Already Logged In
# ==========================================================

if st.session_state.get("logged_in", False):
    redirect_after_login()
    st.stop()

# ==========================================================
# Login Screen
# ==========================================================

st.title("🏥 MSU/EPID Health Coordinator Monitoring System")

st.subheader("Login")

with st.form("login_form", clear_on_submit=False):

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    login_btn = st.form_submit_button(
        "Login",
        use_container_width=True
    )

if login_btn:

    username = username.strip()

    if username == "" or password == "":

        st.error("Username and Password are required.")

    else:

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
