import streamlit as st

from core.session import logout

if (
    "logged_in" not in st.session_state
    or
    not st.session_state.logged_in
):

    st.switch_page("app.py")

if st.session_state.role != "Developer":

    st.error("Access Denied")

    st.stop()

st.title("👨‍💻 Developer Dashboard")

st.write(
    f"Welcome : {st.session_state.full_name}"
)

st.write(
    f"Username : {st.session_state.username}"
)

st.write(
    f"Role : {st.session_state.role}"
)

st.divider()

if st.button("Logout"):

    logout()
