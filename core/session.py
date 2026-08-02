import streamlit as st


DEFAULT_SESSION = {
    "logged_in": False,
    "username": "",
    "role": "",
    "full_name": "",
    "user_id": ""
}


def initialize_session():
    """
    Initialize session variables only once.
    """
    for key, value in DEFAULT_SESSION.items():
        st.session_state.setdefault(key, value)


def login(user: dict):
    """
    Save authenticated user information in session.
    """
    st.session_state["logged_in"] = True
    st.session_state["username"] = user.get("Username", "")
    st.session_state["role"] = user.get("Role", "")
    st.session_state["full_name"] = user.get("Full_Name", "")
    st.session_state["user_id"] = user.get("User_ID", "")


def logout():
    """
    Clear current session and reload app.
    """

    st.session_state.clear()

    initialize_session()

    st.rerun()
