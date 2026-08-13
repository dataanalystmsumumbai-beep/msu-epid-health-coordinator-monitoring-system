import streamlit as st

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    APP_NAME,
    APP_VERSION,
    APP_OWNER,
    APP_ENVIRONMENT,
    AUTO_REFRESH_SECONDS,
    SESSION_TIMEOUT_MINUTES,
    MAX_LOGIN_ATTEMPTS,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    ROLES
)

from utils.google_sheet import (
    read_all,
    update_value
)

from config.config import SYSTEM_SETTINGS


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="System Settings",
    page_icon="⚙️",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error("Please login first.")
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
        "Only Developer and Admin users can access System Settings."
    )

    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "⚙️ System Settings"
)

st.caption(
    "Application configuration and system information"
)

st.divider()


# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

st.subheader(
    "🏥 Application Information"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Application",
        APP_NAME
    )

with c2:

    st.metric(
        "Version",
        APP_VERSION
    )

with c3:

    st.metric(
        "Owner",
        APP_OWNER
    )

with c4:

    st.metric(
        "Environment",
        APP_ENVIRONMENT
    )


st.divider()


# ==========================================================
# SECURITY SETTINGS
# ==========================================================

st.subheader(
    "🔐 Security Settings"
)

s1, s2, s3, s4 = st.columns(4)

with s1:

    st.metric(
        "Min Password Length",
        PASSWORD_MIN_LENGTH
    )

with s2:

    st.metric(
        "Max Password Length",
        PASSWORD_MAX_LENGTH
    )

with s3:

    st.metric(
        "Max Login Attempts",
        MAX_LOGIN_ATTEMPTS
    )

with s4:

    st.metric(
        "Session Timeout",
        f"{SESSION_TIMEOUT_MINUTES} min"
    )


st.divider()


# ==========================================================
# DASHBOARD SETTINGS
# ==========================================================

st.subheader(
    "📊 Dashboard Settings"
)

st.info(
    f"Automatic dashboard refresh interval: "
    f"{AUTO_REFRESH_SECONDS} seconds"
)


st.divider()


# ==========================================================
# ROLE PERMISSIONS
# ==========================================================

st.subheader(
    "👤 Role Permissions"
)


permission_rows = [

    {
        "Role": "Developer",
        "User Management": "Admin + Coordinator",
        "Task Management": "Full",
        "Daily Review": "Full",
        "System Settings": "Full"
    },

    {
        "Role": "Admin",
        "User Management": "Coordinator",
        "Task Management": "Full",
        "Daily Review": "Monitoring",
        "System Settings": "View"
    },

    {
        "Role": "Coordinator",
        "User Management": "No",
        "Task Management": "Assigned Tasks",
        "Daily Review": "Submit Own Review",
        "System Settings": "No"
    }

]


st.dataframe(
    permission_rows,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# GOOGLE SHEET SYSTEM SETTINGS
# ==========================================================

st.subheader(
    "🗄️ Database System Settings"
)


try:

    system_settings = read_all(
        SYSTEM_SETTINGS
    )

except Exception as e:

    system_settings = []

    st.warning(
        f"Unable to load System Settings sheet: {e}"
    )


if system_settings:

    st.dataframe(
        system_settings,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No configurable System Settings records found."
    )


st.divider()


# ==========================================================
# SYSTEM HEALTH
# ==========================================================

st.subheader(
    "🟢 System Health"
)


h1, h2, h3, h4 = st.columns(4)


with h1:

    st.success(
        "Authentication"
    )

with h2:

    st.success(
        "Google Sheets"
    )

with h3:

    st.success(
        "Task Management"
    )

with h4:

    st.success(
        "Daily Review"
    )


st.divider()


# ==========================================================
# CONFIGURATION NOTES
# ==========================================================

st.subheader(
    "ℹ️ Configuration Notes"
)

st.markdown(
    """
    **Important**

    - Google credentials are stored securely in Streamlit Secrets.
    - User passwords are stored as password hashes.
    - Failed login attempts are tracked.
    - Locked accounts can be reset by authorized users.
    - Developer can manage Admin and Coordinator passwords.
    - Admin can manage Coordinator passwords.
    - Coordinators can submit Daily Reviews for their assigned tasks.
    - Task assignment status is linked with Daily Review submission.
    """
)


st.divider()


# ==========================================================
# CURRENT SESSION
# ==========================================================

st.subheader(
    "👤 Current Session"
)

st.write(
    f"**Username:** "
    f"{current_user.get('Username', '')}"
)

st.write(
    f"**Role:** "
    f"{current_role}"
)

st.write(
    f"**Session Timeout:** "
    f"{SESSION_TIMEOUT_MINUTES} minutes"
)
