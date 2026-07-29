import streamlit as st

from core.session import logout

if (
    "logged_in" not in st.session_state
    or
    not st.session_state.logged_in
):

    st.switch_page("app.py")

if st.session_state.role not in [

    "Developer",

    "Admin"

]:

    st.error("Access Denied")

    st.stop()

st.title("👨‍💼 Admin Dashboard")

st.write(

    f"Welcome {st.session_state.full_name}"

)

if st.button("Logout"):

    logout()
