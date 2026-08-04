import streamlit as st

from core.navigation import require_login
from services.user_service import UserService

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

require_login(["Developer", "Admin"])

# ==========================================================
# Header
# ==========================================================

st.title("👥 User Management")

st.caption("Create, Edit, Enable, Disable & Manage Users")

st.divider()

# ==========================================================
# Load Users
# ==========================================================

users = UserService.get_all_users()

if users is None:
    users = []

stats = UserService.statistics()

# ==========================================================
# Dashboard Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("👥 Total Users", stats["total"])

with c2:
    st.metric("👨‍💻 Developers", stats["developers"])

with c3:
    st.metric("👨‍💼 Admins", stats["admins"])

with c4:
    st.metric("🧑‍⚕️ Coordinators", stats["coordinators"])

st.divider()

# ==========================================================
# Tabs
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "👥 User List",
        "➕ Create User",
        "⚙ User Actions"
    ]
)

# ==========================================================
# User List
# ==========================================================

with tab1:

    st.subheader("👥 All Users")

    c1, c2, c3 = st.columns(3)

    with c1:
        search = st.text_input("🔍 Search User")

    with c2:
        role_filter = st.selectbox(
            "Role",
            [
                "All",
                "Developer",
                "Admin",
                "Coordinator"
            ]
        )

    with c3:
        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "ACTIVE",
                "DISABLED",
                "DELETED"
            ]
        )

    filtered = users

    if search.strip():

        txt = search.lower()

        filtered = [

            u

            for u in filtered

            if

            txt in str(u.get("Username","")).lower()

            or

            txt in str(u.get("Full_Name","")).lower()

            or

            txt in str(u.get("Designation","")).lower()

            or

            txt in str(u.get("Mobile","")).lower()

            or

            txt in str(u.get("Email","")).lower()

        ]

    if role_filter != "All":

        filtered = [

            u

            for u in filtered

            if str(u.get("Role","")) == role_filter

        ]

    if status_filter != "All":

        filtered = [

            u

            for u in filtered

            if str(u.get("Status","")).upper() == status_filter

        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"Showing {len(filtered)} of {len(users)} Users"
    )

# ==========================================================
# Create User
# ==========================================================

with tab2:

    st.subheader("➕ Create New User")

    username = st.text_input(
        "Username"
    )

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

    full_name = st.text_input(
        "Full Name"
    )

    designation = st.text_input(
        "Designation"
    )

    mobile = st.text_input(
        "Mobile Number"
    )

    email = st.text_input(
        "Email Address"
    )

    remarks = st.text_area(
        "Remarks"
    )

    c1, c2 = st.columns(2)

    with c1:

        create_btn = st.button(
            "✅ Create User",
            use_container_width=True
        )

    with c2:

        clear_btn = st.button(
            "🔄 Clear",
            use_container_width=True
        )

    if create_btn:

        status, message = UserService.create_user(

            username=username,

            password=password,

            role=role,

            full_name=full_name,

            designation=designation,

            mobile=mobile,

            email=email,

            created_by=st.session_state.get(
                "username",
                "SYSTEM"
            )

        )

        if status:

            st.success(message)

            st.balloons()

            st.rerun()

        else:

            st.error(message)

    if clear_btn:

        st.rerun()

# ==========================================================
# User Actions
# ==========================================================

with tab3:

    st.subheader("⚙ User Actions")

    if len(users) == 0:

        st.warning("No Users Found")

    else:

        user_names = [

            f"{u.get('Username')} ({u.get('Role')})"

            for u in users

        ]

        selected = st.selectbox(

            "Select User",

            range(len(user_names)),

            format_func=lambda x: user_names[x]

        )

        selected_user = users[selected]

        row_no = selected + 2

        current_role = st.session_state.get("role", "")

target_role = selected_user.get("Role", "")

can_manage = True

# Admin cannot manage Developers
if current_role == "Admin" and target_role == "Developer":
    can_manage = False
    

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Username :** {selected_user.get('Username','')}"
            )

            st.write(
                f"**Full Name :** {selected_user.get('Full_Name','')}"
            )

            st.write(
                f"**Role :** {selected_user.get('Role','')}"
            )

            st.write(
                f"**Status :** {selected_user.get('Status','')}"
            )

if not can_manage:

    st.warning(
        "You are not authorized to manage Developer accounts."
    )

else:

       if not can_manage:

    st.warning("You are not authorized to manage Developer accounts.")

else:

    with c2:

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button(
            "🔑 Reset Password",
            use_container_width=True
        ):

            ok, msg = UserService.reset_password(
                row_no,
                new_password,
                st.session_state.get("username", "SYSTEM")
            )

            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "🟢 Enable User",
            use_container_width=True
        ):

            ok, msg = UserService.enable_user(
                row_no,
                st.session_state.get("username", "SYSTEM")
            )

            if ok:
                st.success(msg)
                st.rerun()

    with c2:

        if st.button(
            "🔴 Disable User",
            use_container_width=True
        ):

            ok, msg = UserService.disable_user(
                row_no,
                st.session_state.get("username", "SYSTEM")
            )

            if ok:
                st.success(msg)
                st.rerun()

    with c3:

        if st.button(
            "♻ Unlock Account",
            use_container_width=True
        ):

            ok, msg = UserService.unlock_user(row_no)

            if ok:
                st.success(msg)
                st.rerun()

    st.divider()

    st.subheader("🔄 Change User Role")

    new_role = st.selectbox(
        "New Role",
        [
            "Developer",
            "Admin",
            "Coordinator"
        ]
    )

    if st.button(
        "🔄 Update Role",
        use_container_width=True
    ):

        ok, msg = UserService.change_role(
            row_no,
            new_role,
            st.session_state.get("username", "SYSTEM")
        )

        if ok:
            st.success(msg)
            st.rerun()

    st.divider()

    if st.button(
        "🗑 Archive User",
        use_container_width=True
    ):

        ok, msg = UserService.soft_delete_user(
            row_no,
            st.session_state.get("username", "SYSTEM")
        )

        if ok:
            st.success(msg)
            st.rerun()
            
            new_role = st.selectbox(
            "New Role",
            [
                "Developer",
                "Admin",
                "Coordinator"
            ]
        )

        if st.button(
            "🔄 Update Role",
            use_container_width=True
        ):

            ok, msg = UserService.change_role(
                row_no,
                new_role,
                st.session_state.get(
                    "username",
                    "SYSTEM"
                )
            )

            if ok:

                st.success(msg)

                st.rerun()

        st.divider()

        if st.button(
            "🗑 Archive User",
            use_container_width=True
        ):

            ok, msg = UserService.soft_delete_user(
                row_no,
                st.session_state.get(
                    "username",
                    "SYSTEM"
                )
            )

            if ok:

                st.success(msg)

                st.rerun()
                

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | User Management"
)
