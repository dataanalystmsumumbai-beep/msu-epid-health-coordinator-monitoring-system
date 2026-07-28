import streamlit as st


DEFAULT_SESSION = {
    "logged_in": False,
    "user_id": "",
    "username": "",
    "name": "",
    "role": "",
    "ward": "",
    "login_time": ""
}


def initialize_session():

    for key, value in DEFAULT_SESSION.items():

        if key not in st.session_state:

            st.session_state[key] = value


def login(user):

    st.session_state.logged_in = True
    st.session_state.user_id = user["User_ID"]
    st.session_state.username = user["Username"]
    st.session_state.name = user["Name"]
    st.session_state.role = user["Role"]
    st.session_state.ward = user["Ward"]


def logout():

    for key, value in DEFAULT_SESSION.items():

        st.session_state[key] = value

    st.rerun()
