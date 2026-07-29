import streamlit as st


def initialize_session():

    defaults = {

        "logged_in": False,

        "username": "",

        "role": "",

        "full_name": "",

        "user_id": ""

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def login(user):

    st.session_state.logged_in = True

    st.session_state.username = user["Username"]

    st.session_state.role = user["Role"]

    st.session_state.full_name = user["Full_Name"]

    st.session_state.user_id = user["User_ID"]


def logout():

    st.session_state.clear()

    st.rerun()
