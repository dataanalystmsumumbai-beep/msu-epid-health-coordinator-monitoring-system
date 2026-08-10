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
    ],
    key="user_list_role_filter"
)

    with c3:
        
    status_filter = st.selectbox(
    "Status",
    [
        "All",
        "ACTIVE",
        "DISABLED",
        "DELETED"
    ],
    key="user_list_status_filter"
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
    ],
    key="create_user_role"
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
            f"{u.get('Username', '')} ({u.get('Role', '')})"
            for u in users
        ]

        selected = st.selectbox(
            "Select User",
            range(len(user_names)),
            format_func=lambda x: user_names[x],
            key="user_action_select"
        )

        selected_user = users[selected]

        row_no = selected + 2

        st.divider()

        # ==================================================
        # USER INFORMATION
        # ==================================================

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Username :** {selected_user.get('Username', '')}"
            )

            st.write(
                f"**Full Name :** {selected_user.get('Full_Name', '')}"
            )

            st.write(
                f"**Role :** {selected_user.get('Role', '')}"
            )

            st.write(
                f"**Status :** {selected_user.get('Status', '')}"
            )

        with c2:

            st.write(
                f"**Designation :** {selected_user.get('Designation', '')}"
            )

            st.write(
                f"**Mobile :** {selected_user.get('Mobile', '')}"
            )

            st.write(
                f"**Email :** {selected_user.get('Email', '')}"
            )

        st.divider()

        # ==================================================
        # RESET PASSWORD
        # ==================================================

        st.subheader("🔑 Reset Password")

        new_password = st.text_input(
            "New Password",
            type="password",
            key="user_action_new_password"
        )

        if st.button(
            "🔑 Reset Password",
            use_container_width=True,
            key="reset_password_button"
        ):

            if not new_password.strip():

                st.error("New Password is required.")

            else:

                ok, msg = UserService.reset_password(
                    row_no,
                    new_password,
                    st.session_state.get(
                        "username",
                        "SYSTEM"
                    )
                )

                if ok:

                    st.success(msg)
                    st.rerun()

                else:

                    st.error(msg)

        st.divider()

        # ==================================================
        # ENABLE / DISABLE / UNLOCK
        # ==================================================

        c1, c2, c3 = st.columns(3)

        with c1:

            if st.button(
                "🟢 Enable User",
                use_container_width=True,
                key="enable_user_button"
            ):

                ok, msg = UserService.enable_user(
                    row_no,
                    st.session_state.get(
                        "username",
                        "SYSTEM"
                    )
                )

                if ok:

                    st.success(msg)
                    st.rerun()

                else:

                    st.error(msg)

        with c2:

            if st.button(
                "🔴 Disable User",
                use_container_width=True,
                key="disable_user_button"
            ):

                ok, msg = UserService.disable_user(
                    row_no,
                    st.session_state.get(
                        "username",
                        "SYSTEM"
                    )
                )

                if ok:

                    st.success(msg)
                    st.rerun()

                else:

                    st.error(msg)

        with c3:

            if st.button(
                "♻ Unlock Account",
                use_container_width=True,
                key="unlock_account_button"
            ):

                ok, msg = UserService.unlock_user(
                    row_no
                )

                if ok:

                    st.success(msg)
                    st.rerun()

                else:

                    st.error(msg)

        st.divider()

        # ==================================================
        # CHANGE ROLE
        # ==================================================

        st.subheader("🔄 Change User Role")

        role_options = [
            "Developer",
            "Admin",
            "Coordinator"
        ]

        current_role = selected_user.get(
            "Role",
            "Coordinator"
        )

        new_role = st.selectbox(
            "New Role",
            role_options,
            index=(
                role_options.index(current_role)
                if current_role in role_options
                else 0
            ),
            key="change_user_role"
        )

        if st.button(
            "🔄 Update Role",
            use_container_width=True,
            key="update_role_button"
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

            else:

                st.error(msg)

        st.divider()

        # ==================================================
        # ARCHIVE USER
        # ==================================================

        if st.button(
            "🗑 Archive User",
            use_container_width=True,
            key="archive_user_button"
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

            else:

                st.error(msg)


# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | User Management"
)
