import streamlit as st


# ==========================================================
# ROLE NORMALIZATION
# ==========================================================

def normalize_role(role):

    role = str(
        role or ""
    ).strip().lower()


    role_map = {

        "developer": "Developer",

        "admin": "Admin",

        "administrator": "Admin",

        "coordinator": "Coordinator"

    }


    return role_map.get(
        role,
        ""
    )


# ==========================================================
# LOGIN / PAGE ACCESS
# ==========================================================

def require_login(required_role=None):

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.switch_page(
            "app.py"
        )

        st.stop()


    current_role = normalize_role(
        st.session_state.get(
            "role",
            ""
        )
    )


    st.session_state["role"] = current_role


    if required_role is None:
        return


    if isinstance(
        required_role,
        (list, tuple, set)
    ):

        allowed_roles = [

            normalize_role(role)

            for role in required_role

        ]


        if current_role not in allowed_roles:

            st.error(
                "⛔ Unauthorized Access"
            )

            st.switch_page(
                "app.py"
            )

            st.stop()


        return


    required_role = normalize_role(
        required_role
    )


    if current_role != required_role:

        st.error(
            "⛔ Unauthorized Access"
        )

        st.switch_page(
            "app.py"
        )

        st.stop()


# ==========================================================
# LOGOUT BUTTON
# ==========================================================

def logout_button():

    with st.sidebar:

        st.divider()

        st.markdown(
            "### 👤 Current User"
        )

        full_name = str(
            st.session_state.get(
                "full_name",
                ""
            )
        ).strip()

        username = str(
            st.session_state.get(
                "username",
                ""
            )
        ).strip()

        role = normalize_role(
            st.session_state.get(
                "role",
                ""
            )
        )


        if full_name:

            st.write(
                f"**{full_name}**"
            )

        elif username:

            st.write(
                f"**{username}**"
            )


        if role:

            st.caption(
                f"Role: {role}"
            )


        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="global_logout_button"
        ):

            st.session_state.clear()

            st.rerun()


# ==========================================================
# REDIRECT AFTER LOGIN
# ==========================================================

def redirect_after_login():

    role = normalize_role(
        st.session_state.get(
            "role",
            ""
        )
    )


    st.session_state["role"] = role


    if role == "Developer":

        st.switch_page(
            "pages/00_Developer_Dashboard.py"
        )


    elif role == "Admin":

        st.switch_page(
            "pages/01_Admin_Dashboard.py"
        )


    elif role == "Coordinator":

        st.switch_page(
            "pages/02_Coordinator_Dashboard.py"
        )


    else:

        st.error(
            "Invalid User Role"
        )

        st.stop()


# ==========================================================
# CURRENT USER
# ==========================================================

def current_user():

    return {

        "username":
            st.session_state.get(
                "username",
                ""
            ),

        "full_name":
            st.session_state.get(
                "full_name",
                ""
            ),

        "role":
            normalize_role(
                st.session_state.get(
                    "role",
                    ""
                )
            ),

        "user_id":
            st.session_state.get(
                "user_id",
                ""
            )

    }
