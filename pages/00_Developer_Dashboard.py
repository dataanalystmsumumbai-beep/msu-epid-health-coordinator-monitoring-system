import streamlit as st

from services.user_service import UserService

st.title("👨‍💻 Developer Dashboard")

tab1, tab2 = st.tabs([
    "📊 Dashboard",
    "👤 Create User"
])

with tab1:

    users = UserService.get_all_users()

    st.metric(
        "Total Users",
        len(users)
    )

    st.dataframe(
        users,
        use_container_width=True
    )


with tab2:

    st.subheader("Create New User")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        [
            "Developer",
            "Admin",
            "Coordinator"
        ]
    )

    full_name = st.text_input("Full Name")

    designation = st.text_input("Designation")

    mobile = st.text_input("Mobile")

    email = st.text_input("Email")

    if st.button(
        "Create User",
        use_container_width=True
    ):

        status, message = UserService.create_user(

            username=username,
            password=password,
            role=role,
            full_name=full_name,
            designation=designation,
            mobile=mobile,
            email=email,
            created_by=st.session_state.username

        )

        if status:

            st.success(message)

            st.rerun()

        else:

            st.error(message)
