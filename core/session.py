import streamlit as st


SESSION_DEFAULTS = {

    "logged_in": False,

    "username": "",

    "name": "",

    "role": "",

    "user_id": "",

    "ward": "",

    "login_time": "",

}


def initialize_session():

    for key, value in SESSION_DEFAULTS.items():

        if key not in st.session_state:

            st.session_state[key] = value


def logout():

    for key in SESSION_DEFAULTS.keys():

        st.session_state[key] = SESSION_DEFAULTS[key]

    st.rerun()
