import streamlit as st

from core.navigation import require_login
from services.user_service import UserService


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

require_login(["Developer", "Admin"])


# ==========================================================
# HEADER
# ==========================================================

st.title("👥 User Management")

st.caption(
    "Create, Edit, Enable, Disable & Manage Users"
)

st.divider()


# ==========================================================
# LOAD USERS
# ==========================================================

users = UserService.get_all_users()

if users is None:
    users = []

stats = UserService.statistics()


# ==========================================================
# DASHBOARD CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👥 Total Users",
        stats["total"]
    )

with c2:
    st.metric(
        "👨‍💻 Developers",
        stats["developers"]
    )

with c3:
    st.metric(
        "👨‍💼 Admins",
        stats["admins"]
    )

with c4:
    st.metric(
        "🧑‍⚕️ Coordinators",
        stats["coordinators"]
    )


st.divider()


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "👥 User List",
        "➕ Create User",
        "⚙ User Actions"
    ]
)


# ==========================================================
# TAB 1 — USER LIST
# ==========================================================

with tab1:

    st.subheader("👥 All Users")

    c1, c2, c3 = st.columns(3)

    with c1:

        search = st.text_input(
            "🔍 Search User",
            key="user_search"
        )

    with c2:

        role_filter = st.selectbox(
            "Role",
            [
                "All",
                "Developer",
                "Admin",
                "Coordinator"
            ],
            key="user_role_filter"
        )

    with c3:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "ACTIVE",
                "INACTIVE",
                "DELETED"
            ],
            key="user_status_filter"
        )

    filtered = users

    if search.strip():

        search_text = search.strip().lower()

        filtered = [

            user

            for user in filtered

            if (

                search_text
                in str(
                    user.get(
                        "Username",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    user.get(
                        "Full_Name",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    user.get(
                        "Designation",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    user.get(
                        "Mobile",
                        ""
                    )
                ).lower()

                or

                search_text
                in str(
                    user.get(
                        "Email",
                        ""
                    )
                ).lower()

            )

        ]

    if role_filter != "All":

        filtered = [

            user

            for user in filtered

            if str(
                user.get(
                    "Role",
                    ""
                )
            ).strip()
            == role_filter

        ]

    if status_filter != "All":

        filtered = [

            user

            for user in filtered

            if str(
                user.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == status_filter

        ]

    if filtered:

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No users found."
        )

    st.caption(
        f"Showing {len(filtered)} of {len(users)} users"
    )


# ==========================================================
# TAB 2 — CREATE USER
# ==========================================================

with tab2:

    st.subheader("➕ Create New User")

    username = st.text_input(
        "Username",
        key="create_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="create_password"
    )

    role = st.selectbox(
        "Role",
        [
            "Developer",
            "Admin",
            "Coordinator"
        ],
        key="create_role"
    )

    full_name = st.text_input(
        "Full Name",
        key="create_full_name"
    )

    designation = st.text_input(
        "Designation",
        key="create_designation"
    )

    mobile = st.text_input(
        "Mobile Number",
        key="create_mobile"
    )

    email = st.text_input(
        "Email Address",
        key="create_email"
    )

    remarks = st.text_area(
        "Remarks",
        key="create_remarks"
    )

    c1, c2 = st.columns(2)

    with c1:

        create_btn = st.button(
            "✅ Create User",
            use_container_width=True,
            key="create_user_btn"
        )

    with c2:

        clear_btn = st.button(
            "🔄 Clear",
            use_container_width=True,
            key="clear_user_btn"
        )

    if create_btn:

        current_role = str(
            st.session_state.get(
                "role",
                ""
            )
        ).strip()

        if (
            current_role == "Admin"
            and role == "Developer"
        ):

            st.error(
                "Admin cannot create Developer accounts."
            )

        else:

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

                st.rerun()

            else:

                st.error(message)

    if clear_btn:

        st.rerun()


# ==========================================================
# TAB 3 — USER ACTIONS
# ==========================================================

with tab3:

    st.subheader("⚙ User Actions")

    if not users:

        st.warning(
            "No Users Found."
        )

    else:

        user_names = [

            f"{user.get('Username', '')} "
            f"({user.get('Role', '')})"

            for user in users

        ]

        selected_index = st.selectbox(

            "Select User",

            range(len(user_names)),

            format_func=lambda x:
            user_names[x],

            key="selected_user"

        )

        selected_user = users[selected_index]

        row_no = selected_index + 2

        current_role = str(
            st.session_state.get(
                "role",
                ""
            )
        ).strip()

        target_role = str(
            selected_user.get(
                "Role",
                ""
            )
        ).strip()

        target_username = str(
            selected_user.get(
                "Username",
                ""
            )
        ).strip()

        logged_username = str(
            st.session_state.get(
                "username",
                ""
            )
        ).strip()

        can_manage = False

        if current_role == "Developer":

            can_manage = True

        elif current_role == "Admin":

            if target_role in [
                "Admin",
                "Coordinator"
            ]:

                can_manage = True

        if (
            target_username.lower()
            == logged_username.lower()
        ):

            can_manage = False

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Username:** "
                f"{selected_user.get('Username', '')}"
            )

            st.write(
                f"**Full Name:** "
                f"{selected_user.get('Full_Name', '')}"
            )

            st.write(
                f"**Role:** "
                f"{selected_user.get('Role', '')}"
            )

            st.write(
                f"**Status:** "
                f"{selected_user.get('Status', '')}"
            )

        with c2:

            st.write(
                f"**Designation:** "
                f"{selected_user.get('Designation', '')}"
            )

            st.write(
                f"**Mobile:** "
                f"{selected_user.get('Mobile', '')}"
            )

            st.write(
                f"**Email:** "
                f"{selected_user.get('Email', '')}"
            )

            st.write(
                f"**Account Locked:** "
                f"{selected_user.get('Account_Locked', '')}"
            )

        if not can_manage:

            if (
                target_username.lower()
                == logged_username.lower()
            ):

                st.info(
                    "You cannot manage your own account."
                )

            elif (
                current_role == "Admin"
                and target_role == "Developer"
            ):

                st.warning(
                    "Admin cannot manage Developer accounts."
                )

            else:

                st.warning(
                    "You are not authorized "
                    "to manage this account."
                )

        else:

            # ==================================================
            # PASSWORD RESET
            # ==================================================

            st.divider()

            st.subheader(
                "🔑 Reset Password"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )

            if st.button(
                "🔑 Reset Password",
                use_container_width=True,
                key="reset_password"
            ):

                if not new_password.strip():

                    st.error(
                        "New Password is required."
                    )

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


            # ==================================================
            # ACCOUNT ACTIONS
            # ==================================================

            st.divider()

            st.subheader(
                "🔐 Account Actions"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                if st.button(
                    "🟢 Enable User",
                    use_container_width=True,
                    key="enable_user"
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
                    key="disable_user"
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
                    key="unlock_user"
                ):

                    ok, msg = UserService.unlock_user(
                        row_no
                    )

                    if ok:

                        st.success(msg)

                        st.rerun()

                    else:

                        st.error(msg)


            # ==================================================
            # ROLE CHANGE
            # ==================================================

            st.divider()

            st.subheader(
                "🔄 Change User Role"
            )

            if current_role == "Developer":

                role_options = [
                    "Developer",
                    "Admin",
                    "Coordinator"
                ]

            else:

                role_options = [
                    "Admin",
                    "Coordinator"
                ]

            if target_role in role_options:

                role_index = role_options.index(
                    target_role
                )

            else:

                role_index = 0

            new_role = st.selectbox(

                "New Role",

                role_options,

                index=role_index,

                key="new_user_role"

            )

            if st.button(
                "🔄 Update Role",
                use_container_width=True,
                key="update_user_role"
            ):

                if new_role == target_role:

                    st.info(
                        "Selected role is already assigned."
                    )

                else:

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


            # ==================================================
            # ARCHIVE USER
            # ==================================================

            st.divider()

            if st.button(
                "🗑 Archive User",
                use_container_width=True,
                key="archive_user"
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
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System "
    "| User Management"
)
