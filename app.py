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


# ==========================================================
# Global Navigation
# ==========================================================

pages = [
    st.Page(
        "pages/00_Developer_Dashboard.py",
        title="Developer Dashboard"
    ),
    st.Page(
        "pages/01_Admin_Dashboard.py",
        title="Admin Dashboard"
    ),
    st.Page(
        "pages/02_Coordinator_Dashboard.py",
        title="Coordinator Dashboard"
    ),
    st.Page(
        "pages/03_Daily_Review.py",
        title="Daily Review"
    ),
    st.Page(
        "pages/04_Task_Management.py",
        title="Task Management"
    ),
    st.Page(
        "pages/05_User_Management.py",
        title="User Management"
    ),
    st.Page(
        "pages/06_Help_Center.py",
        title="Help Center"
    ),
    st.Page(
        "pages/07_System_Settings.py",
        title="System Settings"
    ),
    st.Page(
        "pages/08_System_Manual.py",
        title="System Manual"
    ),
    st.Page(
        "pages/09_Notifications.py",
        title="Notifications"
    ),
    st.Page(
        "pages/10_Reports_Dashboard.py",
        title="Reports Dashboard"
    ),
    st.Page(
        "pages/11_System_Status.py",
        title="System Status"
    ),
    st.Page(
        "pages/12_About.py",
        title="About"
    ),
    st.Page(
        "pages/13_Contact_Support.py",
        title="Contact Support"
    )
]

pg = st.navigation(pages)


# ==========================================================
# Global Sidebar Signature
# ==========================================================

with st.sidebar:

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align: center;
            color: #777;
            font-size: 11px;
            line-height: 1.5;
            padding: 8px 4px 4px 4px;
        ">
            <b>App Made By:</b><br>
            Data Analyst<br><br>
            <b>Institution:</b><br>
            Metropolitan Surveillance Unit (MSU), Mumbai
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# Session Initialization
# ==========================================================

initialize_session()


# ==========================================================
# Already Logged In
# ==========================================================

if st.session_state.get("logged_in", False):

    pg.run()

    st.stop()


# ==========================================================
# Login Screen
# ==========================================================

st.title(
    "🏥 MSU/EPID Health Coordinator Monitoring System"
)

st.markdown(
    """
    <div style="
        font-size: 13px;
        color: #666;
        margin-top: -10px;
        margin-bottom: 20px;
    ">
        <b>App Made By:</b> Data Analyst &nbsp; | &nbsp;
        <b>Institution:</b> Metropolitan Surveillance Unit (MSU), Mumbai
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Login")


with st.form(
    "login_form",
    clear_on_submit=False
):

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

        st.error(
            "Username and Password are required."
        )

    else:

        status, result = AuthService.authenticate(
            username,
            password
        )

        if status:

            login(result)

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(result)
