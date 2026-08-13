import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

from core.navigation import require_login

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)

from config.config import (
    USERS,
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)


# ==========================================================
# ACCESS
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN
])


# ==========================================================
# SESSION
# ==========================================================

current_role = str(
    st.session_state.get("role", "")
).strip()

current_user_id = str(
    st.session_state.get("user_id", "")
).strip()

current_username = str(
    st.session_state.get("username", "")
).strip()


# ==========================================================
# HELPERS
# ==========================================================

def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def get_value(row, *keys):

    for key in keys:

        value = row.get(
            key,
            ""
        )

        if value is not None and clean(value):

            return clean(value)

    return ""


def can_manage_user(target_role):

    target_role = clean(
        target_role
    ).lower()

    current = clean(
        current_role
    ).lower()

    if current == "developer":
        return target_role in [
            "developer",
            "admin",
            "coordinator"
        ]

    if current == "admin":
        return target_role == "coordinator"

    return False


def can_disable_user(target_role):

    return can_manage_user(
        target_role
    )


# ==========================================================
# LOAD USERS
# ==========================================================

try:

    users = read_all(
        USERS
    )

except Exception:

    users = []


users = users or []


# ==========================================================
# HEADER
# ==========================================================

st.title("👥 User Management")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# METRICS
# ==========================================================

active_users = [
    user
    for user in users
    if clean(
        get_value(
            user,
            "Status"
        )
    ).upper()
    == "ACTIVE"
]


developers = [
    user
    for user in users
    if clean(
        get_value(
            user,
            "Role"
        )
    ).lower()
    == "developer"
]


admins = [
    user
    for user in users
    if clean(
        get_value(
            user,
            "Role"
        )
    ).lower()
    == "admin"
]


coordinators = [
    user
    for user in users
    if clean(
        get_value(
            user,
            "Role"
        )
    ).lower()
    == "coordinator"
]


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👥 Total Users",
        len(users)
    )

with c2:
    st.metric(
        "👨‍💻 Developers",
        len(developers)
    )

with c3:
    st.metric(
        "🧑‍💼 Admins",
        len(admins)
    )

with c4:
    st.metric(
        "👨‍⚕️ Coordinators",
        len(coordinators)
    )


st.divider()


# ==========================================================
# TABS
# ==========================================================

tab_users, tab_create, tab_actions = st.tabs(
    [
        "👥 User List",
        "➕ Create User",
        "⚙️ User Actions"
    ]
)


# ==========================================================
# USER LIST
# ==========================================================

with tab_users:

    st.subheader(
        "👥 All Users"
    )

    search = st.text_input(
        "🔎 Search User",
        key="user_search"
    )

    role_filter = st.selectbox(
        "Role",
        [
            "All",
            "Developer",
            "Admin",
            "Coordinator"
        ],
        key="role_filter"
    )

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "ACTIVE",
            "DISABLED"
        ],
        key="status_filter"
    )


    filtered_users = []

    for user in users:

        username = get_value(
            user,
            "Username"
        )

        full_name = get_value(
            user,
            "Full_Name",
            "Full Name"
        )

        role = get_value(
            user,
            "Role"
        )

        status = get_value(
            user,
            "Status"
        )


        if search:

            search_text = (
                username
                + " "
                + full_name
                + " "
                + role
            ).lower()

            if search.lower() not in search_text:

                continue


        if role_filter != "All":

            if role.lower() != role_filter.lower():

                continue


        if status_filter != "All":

            if status.upper() != status_filter.upper():

                continue


        filtered_users.append(
            user
        )


    rows = []

    for user in filtered_users:

        rows.append(
            {
                "User_ID":
                    get_value(
                        user,
                        "User_ID",
                        "User_Id"
                    ),

                "Username":
                    get_value(
                        user,
                        "Username"
                    ),

                "Role":
                    get_value(
                        user,
                        "Role"
                    ),

                "Full_Name":
                    get_value(
                        user,
                        "Full_Name",
                        "Full Name"
                    ),

                "Designation":
                    get_value(
                        user,
                        "Designation"
                    ),

                "Mobile":
                    get_value(
                        user,
                        "Mobile"
                    ),

                "Email":
                    get_value(
                        user,
                        "Email"
                    ),

                "Status":
                    get_value(
                        user,
                        "Status"
                    ),

                "Last_Login":
                    get_value(
                        user,
                        "Last_Login",
                        "Last Login"
                    ),

                "Password_Changed":
                    get_value(
                        user,
                        "Password_Changed"
                    ),

                "Login_Attempts":
                    get_value(
                        user,
                        "Login_Attempts"
                    ),

                "Account_Locked":
                    get_value(
                        user,
                        "Account_Locked"
                    )
            }
        )


    if rows:

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            f"Showing {len(rows)} of {len(users)} users"
        )

    else:

        st.info(
            "No users found."
        )


# ==========================================================
# CREATE USER
# ==========================================================

with tab_create:

    st.subheader(
        "➕ Create New User"
    )


    new_role_options = [
        "Coordinator"
    ]

    if current_role.lower() == "developer":

        new_role_options = [
            "Admin",
            "Coordinator"
        ]


    new_role = st.selectbox(
        "Role",
        new_role_options,
        key="new_user_role"
    )


    col1, col2 = st.columns(2)

    with col1:

        new_username = st.text_input(
            "Username",
            key="new_username"
        )

        new_full_name = st.text_input(
            "Full Name",
            key="new_full_name"
        )

        new_designation = st.text_input(
            "Designation",
            key="new_designation"
        )


    with col2:

        new_mobile = st.text_input(
            "Mobile",
            key="new_mobile"
        )

        new_email = st.text_input(
            "Email",
            key="new_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="new_password"
        )


    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_new_password"
    )


    create_button = st.button(
        "➕ Create User",
        type="primary",
        use_container_width=True,
        key="create_user_button"
    )


    if create_button:

        if not new_username.strip():

            st.error(
                "Username is required."
            )

        elif not new_full_name.strip():

            st.error(
                "Full Name is required."
            )

        elif not new_password:

            st.error(
                "Password is required."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            username_exists = any(
                clean(
                    get_value(
                        user,
                        "Username"
                    )
                ).lower()
                == new_username.strip().lower()

                for user in users
            )


            if username_exists:

                st.error(
                    "Username already exists."
                )

            else:

                existing_ids = []

                for user in users:

                    uid = get_value(
                        user,
                        "User_ID",
                        "User_Id"
                    )

                    if uid:
                        existing_ids.append(uid)


                if new_role.lower() == "admin":

                    prefix = "USRADM"

                else:

                    prefix = "USRCO"


                numeric_part = (
                    len(existing_ids)
                    + 1
                )

                new_user_id = (
                    f"{prefix}{numeric_part:03d}"
                )


                row = [

                    new_user_id,

                    new_username.strip(),

                    hash_password(
                        new_password
                    ),

                    new_role,

                    new_full_name.strip(),

                    new_designation.strip(),

                    new_mobile.strip(),

                    new_email.strip(),

                    "ACTIVE",

                    "",

                    "YES",

                    "NO",

                    0,

                    "NO",

                    datetime.now().strftime(
                        "%d-%m-%Y"
                    ),

                    current_username,

                    "",

                    "",

                    ""

                ]


                try:

                    insert_row(
                        USERS,
                        row
                    )

                    st.success(
                        "User created successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to create user: {e}"
                    )


# ==========================================================
# USER ACTIONS
# ==========================================================

with tab_actions:

    st.subheader(
        "⚙️ User Actions"
    )


    manageable_users = []

    for user in users:

        target_role = get_value(
            user,
            "Role"
        )

        target_user_id = get_value(
            user,
            "User_ID",
            "User_Id"
        )

        if not target_user_id:

            continue


        if not can_manage_user(
            target_role
        ):

            continue


        if (
            target_user_id
            == current_user_id
        ):

            continue


        manageable_users.append(
            user
        )


    if not manageable_users:

        st.info(
            "No users are available for management."
        )

    else:

        user_options = {}

        for user in manageable_users:

            uid = get_value(
                user,
                "User_ID",
                "User_Id"
            )

            username = get_value(
                user,
                "Username"
            )

            role = get_value(
                user,
                "Role"
            )

            full_name = get_value(
                user,
                "Full_Name",
                "Full Name"
            )

            user_options[
                uid
            ] = (
                f"{full_name or username} "
                f"| {username} "
                f"| {role}"
            )


        selected_user_id = st.selectbox(
            "Select User",
            list(
                user_options.keys()
            ),
            format_func=lambda x:
                user_options[x],
            key="selected_manage_user"
        )


        selected_user = next(
            (
                user

                for user in manageable_users

                if get_value(
                    user,
                    "User_ID",
                    "User_Id"
                )
                == selected_user_id
            ),
            {}
        )


        selected_role = get_value(
            selected_user,
            "Role"
        )

        selected_username = get_value(
            selected_user,
            "Username"
        )

        selected_status = get_value(
            selected_user,
            "Status"
        )


        st.write(
            f"**Username:** {selected_username}"
        )

        st.write(
            f"**Role:** {selected_role}"
        )

        st.write(
            f"**Current Status:** {selected_status}"
        )


        st.divider()


        # ==================================================
        # PASSWORD RESET
        # ==================================================

        st.markdown(
            "### 🔐 Change Password"
        )


        new_password_admin = st.text_input(
            "New Password",
            type="password",
            key="admin_new_password"
        )


        confirm_password_admin = st.text_input(
            "Confirm New Password",
            type="password",
            key="admin_confirm_password"
        )


        if st.button(
            "🔐 Change Password",
            type="primary",
            use_container_width=True,
            key="change_user_password"
        ):

            if not new_password_admin:

                st.error(
                    "New password is required."
                )

            elif (
                new_password_admin
                != confirm_password_admin
            ):

                st.error(
                    "Passwords do not match."
                )

            else:

                password_hash = hash_password(
                    new_password_admin
                )


                password_column = 2

                modified_on_column = 16

                modified_by_column = 17


                try:

                    update_value(
                        USERS,
                        selected_user.get(
                            "_row",
                            selected_user.get(
                                "row",
                                0
                            )
                        ),
                        password_column,
                        password_hash
                    )


                    update_value(
                        USERS,
                        selected_user.get(
                            "_row",
                            selected_user.get(
                                "row",
                                0
                            )
                        ),
                        modified_on_column,
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    )


                    update_value(
                        USERS,
                        selected_user.get(
                            "_row",
                            selected_user.get(
                                "row",
                                0
                            )
                        ),
                        modified_by_column,
                        current_username
                    )


                    st.success(
                        "Password changed successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Unable to change password: {e}"
                    )


        st.divider()


        # ==================================================
        # ENABLE / DISABLE
        # ==================================================

        if can_disable_user(
            selected_role
        ):

            st.markdown(
                "### 🔄 Account Status"
            )


            if selected_status.upper() == "ACTIVE":

                if st.button(
                    "🚫 Disable User",
                    use_container_width=True,
                    key="disable_selected_user"
                ):

                    try:

                        row_number = selected_user.get(
                            "_row",
                            selected_user.get(
                                "row",
                                0
                            )
                        )


                        update_value(
                            USERS,
                            row_number,
                            9,
                            "DISABLED"
                        )


                        st.success(
                            "User disabled successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Unable to disable user: {e}"
                        )

            else:

                if st.button(
                    "✅ Enable User",
                    use_container_width=True,
                    key="enable_selected_user"
                ):

                    try:

                        row_number = selected_user.get(
                            "_row",
                            selected_user.get(
                                "row",
                                0
                            )
                        )


                        update_value(
                            USERS,
                            row_number,
                            9,
                            "ACTIVE"
                        )


                        st.success(
                            "User enabled successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Unable to enable user: {e}"
                        )
