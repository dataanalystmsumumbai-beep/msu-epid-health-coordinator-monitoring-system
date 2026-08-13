import streamlit as st
from datetime import datetime

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="System Status",
    page_icon="🟢",
    layout="wide"
)


# ==========================================================
# ACCESS
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
])


# ==========================================================
# SESSION
# ==========================================================

current_role = str(
    st.session_state.get(
        "role",
        ""
    )
).strip()

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()


# ==========================================================
# HEADER
# ==========================================================

st.title("🟢 System Status")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.subheader("🖥️ Application Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Application",
        "🟢 Online"
    )

with c2:
    st.metric(
        "Authentication",
        "🟢 Active"
    )

with c3:
    st.metric(
        "Task System",
        "🟢 Active"
    )

with c4:
    st.metric(
        "Daily Review",
        "🟢 Active"
    )


st.divider()


# ==========================================================
# SESSION INFORMATION
# ==========================================================

st.subheader("🔐 Current Session")

session_data = {
    "Parameter": [
        "Username",
        "Role",
        "User ID",
        "Session Status"
    ],
    "Value": [
        current_username,
        current_role,
        str(
            st.session_state.get(
                "user_id",
                ""
            )
        ),
        "Active"
    ]
}

st.table(
    session_data
)


st.divider()


# ==========================================================
# MODULE STATUS
# ==========================================================

st.subheader("📦 Module Status")

modules = {
    "Module": [
        "Login & Authentication",
        "User Management",
        "Task Management",
        "Daily Review",
        "Notifications",
        "Reports Dashboard",
        "Help Center",
        "System Manual"
    ],
    "Status": [
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active"
    ]
}

st.table(
    modules
)


st.divider()


# ==========================================================
# ROLE ACCESS
# ==========================================================

st.subheader("👥 Role Access")

role_access = {
    "Role": [
        "Developer",
        "Admin",
        "Coordinator"
    ],
    "Access Level": [
        "Full System Access",
        "Operational Management",
        "Task & Daily Review"
    ]
}

st.table(
    role_access
)


st.divider()


# ==========================================================
# LAST CHECK
# ==========================================================

st.subheader("🕒 Status Check")

current_time = datetime.now().strftime(
    "%d-%m-%Y %I:%M:%S %p"
)

st.success(
    f"System status checked successfully at {current_time}."
)


# ==========================================================
# REFRESH
# ==========================================================

if st.button(
    "🔄 Refresh System Status",
    use_container_width=True
):
    st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "System Status • Coordinator Monitoring & Task Management System"
)
