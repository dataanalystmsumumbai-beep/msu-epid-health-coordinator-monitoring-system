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
    """
    Protect application pages from unauthorized access.
    Supports a single role or a list of allowed roles.
    """

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


    # Keep normalized role in session
    st.session_state["role"] = current_role


    # ------------------------------------------------------
    # No specific role restriction
    # ------------------------------------------------------

    if required_role is None:

        return


    # ------------------------------------------------------
    # Multiple allowed roles
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Single allowed role
    # ------------------------------------------------------

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
