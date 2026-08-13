import streamlit as st


# ==========================================================
# DEFAULT SESSION
# ==========================================================

DEFAULT_SESSION = {
    "logged_in": False,
    "username": "",
    "role": "",
    "full_name": "",
    "user_id": "",
    "user": {}
}


# ==========================================================
# INITIALIZE SESSION
# ==========================================================

def initialize_session():

    for key, value in DEFAULT_SESSION.items():

        st.session_state.setdefault(
            key,
            value
        )


# ==========================================================
# LOGIN
# ==========================================================

def login(user: dict):

    # ------------------------------------------------------
    # Store complete user object
    # ------------------------------------------------------

    st.session_state["user"] = dict(user)

    # ------------------------------------------------------
    # Store individual session values
    # ------------------------------------------------------

    st.session_state["logged_in"] = True

    st.session_state["username"] = str(
        user.get(
            "Username",
            ""
        )
    ).strip()

    st.session_state["role"] = str(
        user.get(
            "Role",
            ""
        )
    ).strip()

    st.session_state["full_name"] = str(
        user.get(
            "Full_Name",
            ""
        )
    ).strip()

    st.session_state["user_id"] = str(
        user.get(
            "User_ID",
            ""
        )
    ).strip()


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    st.session_state.clear()

    initialize_session()

    st.rerun()
