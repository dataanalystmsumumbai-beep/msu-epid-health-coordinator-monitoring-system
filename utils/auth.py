import streamlit as st

def login(username, password):
    return False

def logout():
    if "logged_in" in st.session_state:
        del st.session_state["logged_in"]

def is_logged_in():
    return st.session_state.get("logged_in", False)
