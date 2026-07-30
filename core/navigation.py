import streamlit as st


def require_login(required_role=None):
    """
    Protects every page from direct access.
    """

    if not st.session_state.get("logged_in", False):
        st.switch_page("app.py")
        st.stop()

    if required_role:

        current_role = st.session_state.get("role", "")

        if current_role != required_role:
            st.error("⛔ Unauthorized Access")
            st.switch_page("app.py")
            st.stop()


def redirect_after_login():

    role = st.session_state.get("role", "")

    if role == "Developer":
        st.switch_page("pages/00_Developer_Dashboard.py")

    elif role == "Admin":
        st.switch_page("pages/01_Admin_Dashboard.py")

    elif role == "Coordinator":
        st.switch_page("pages/02_Coordinator_Dashboard.py")

    else:
        st.error("Invalid User Role")
        st.stop()


def current_user():

    return {
        "username": st.session_state.get("username", ""),
        "full_name": st.session_state.get("full_name", ""),
        "role": st.session_state.get("role", ""),
        "user_id": st.session_state.get("user_id", "")
    }
