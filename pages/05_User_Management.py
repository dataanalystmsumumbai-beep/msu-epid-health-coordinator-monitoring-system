import streamlit as st

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    USER_MASTER
)

from utils.google_sheet import (
    read_all,
    update_value
)

from utils.security import (
    hash_password
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error(
        "Please login first."
    )

    st.stop()


# ==========================================================
# CURRENT USER
# ==========================================================

current_user = st.session_state.get(
    "user",
    {}
)

current_role = str(
    current_user.get(
        "Role",
        ""
    )
).strip()


# ==========================================================
# ACCESS CONTROL
# ==========================================================

if current_role not in [
    ROLE_DEVELOPER,
    ROLE_ADMIN
]:

    st.error(
        "You do not have permission to access User Management."
    )

    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "👥 User Management"
)

st.caption(
    "Manage user accounts and passwords"
)

st.divider()


# ==========================================================
# LOAD USERS
# ==========================================================

try:

    users = read_all(
        USER_MASTER
    )

except Exception as e:

    st.error(
        f"Unable to load users: {e}"
    )

    st.stop()


if not users:

    st.info(
        "No users found."
    )

    st.stop()


# ==========================================================
# CURRENT USERNAME
# ==========================================================

current_username = str(
    current_user.get(
        "Username",
        ""
    )
).strip().lower()


# ==========================================================
# PASSWORD CHANGE
# ==========================================================

st.subheader(
    "🔐 Change User Password"
)


# ----------------------------------------------------------
# FILTER USERS ACCORDING TO ROLE
# ----------------------------------------------------------

allowed_users = []


for row_number, user in enumerate(
    users,
    start=2
):

    username = str(
        user.get(
            "Username",
            ""
        )
    ).strip()

    role = str(
        user.get(
            "Role",
            ""
        )
    ).strip()

    status = str(
        user.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()


    if not username:

        continue


    # ------------------------------------------------------
    # DEVELOPER
    # Developer can manage Admin + Coordinator
    # ------------------------------------------------------

    if current_role == ROLE_DEVELOPER:

        if role in [
            ROLE_ADMIN,
            ROLE_COORDINATOR
        ]:

            allowed_users.append(
                (
                    row_number,
                    user
                )
            )


    # ------------------------------------------------------
    # ADMIN
    # Admin can manage Coordinator only
    # ------------------------------------------------------

    elif current_role == ROLE_ADMIN:

        if role == ROLE_COORDINATOR:

            allowed_users.append(
                (
                    row_number,
                    user
                )
            )


# ==========================================================
# USER SELECTION
# ==========================================================

if not allowed_users:

    st.info(
        "No users are available for password management."
    )

else:

    user_options = {}


    for row_number, user in allowed_users:

        username = str(
            user.get(
                "Username",
                ""
            )
        ).strip()

        role = str(
            user.get(
                "Role",
                ""
            )
        ).strip()

        user_options[
            f"{username} ({role})"
        ] = row_number


    selected_label = st.selectbox(

        "Select User",

        list(
            user_options.keys()
        ),

        key="password_user_select"

    )


    selected_row = user_options[
        selected_label
    ]


    selected_user = users[
        selected_row - 2
    ]


    selected_username = str(
        selected_user.get(
            "Username",
            ""
        )
    ).strip()


    selected_role = str(
        selected_user.get(
            "Role",
            ""
        )
    ).strip()


    st.info(
        f"Selected User: "
        f"**{selected_username}** "
        f"| Role: **{selected_role}**"
    )


    # ======================================================
    # NEW PASSWORD
    # ======================================================

    new_password = st.text_input(

        "New Password",

        type="password",

        key="new_user_password"

    )


    confirm_password = st.text_input(

        "Confirm New Password",

        type="password",

        key="confirm_user_password"

    )


    # ======================================================
    # CHANGE PASSWORD
    # ======================================================

    if st.button(

        "🔑 Update Password",

        type="primary",

        use_container_width=True,

        key="update_user_password"

    ):

        if not new_password:

            st.error(
                "Please enter a new password."
            )

        elif len(new_password) < 8:

            st.error(
                "Password must contain at least 8 characters."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            try:

                password_hash = hash_password(
                    new_password
                )


                # --------------------------------------------------
                # Password_Hash column
                # --------------------------------------------------

                password_column = 5


                update_value(

                    USER_MASTER,

                    selected_row,

                    password_column,

                    password_hash

                )


                # --------------------------------------------------
                # Reset Login Attempts
                # --------------------------------------------------

                update_value(

                    USER_MASTER,

                    selected_row,

                    12,

                    0

                )


                # --------------------------------------------------
                # Unlock Account
                # --------------------------------------------------

                update_value(

                    USER_MASTER,

                    selected_row,

                    13,

                    "NO"

                )


                st.success(

                    f"Password updated successfully "
                    f"for {selected_username}."

                )

                st.rerun()


            except Exception as e:

                st.error(

                    f"Unable to update password: {e}"

                )


# ==========================================================
# USER STATUS MONITOR
# ==========================================================

st.divider()

st.subheader(
    "👥 User Account Status"
)


status_rows = []


for row_number, user in enumerate(
    users,
    start=2
):

    username = str(
        user.get(
            "Username",
            ""
        )
    ).strip()

    role = str(
        user.get(
            "Role",
            ""
        )
    ).strip()

    status = str(
        user.get(
            "Status",
            ""
        )
    ).strip()

    locked = str(
        user.get(
            "Account_Locked",
            "NO"
        )
    ).strip()


    # ------------------------------------------------------
    # Visibility rules
    # ------------------------------------------------------

    if current_role == ROLE_DEVELOPER:

        visible = role in [
            ROLE_ADMIN,
            ROLE_COORDINATOR
        ]

    else:

        visible = role == ROLE_COORDINATOR


    if not visible:

        continue


    status_rows.append(
        {
            "Username": username,
            "Role": role,
            "Status": status,
            "Account Locked": locked
        }
    )


if status_rows:

    st.dataframe(

        status_rows,

        use_container_width=True,

        hide_index=True

    )

else:

    st.info(
        "No user accounts available."
    )

