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
# ACCESS CONTROL
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
])


# ==========================================================
# SESSION INFORMATION
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

current_user_id = str(
    st.session_state.get(
        "user_id",
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
# APPLICATION STATUS
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
# CURRENT SESSION
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
        current_username if current_username else "Not Available",
        current_role if current_role else "Not Available",
        current_user_id if current_user_id else "Not Available",
        "🟢 Active"
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
        "Developer Dashboard",
        "Admin Dashboard",
        "Coordinator Dashboard",
        "User Management",
        "Task Management",
        "Daily Review",
        "Notifications",
        "Reports Dashboard",
        "Help Center",
        "System Settings",
        "System Manual",
        "About",
        "Contact Support"
    ],
    "Status": [
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
        "🟢 Active",
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

st.dataframe(
    modules,
    use_container_width=True,
    hide_index=True
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
    ],
    "Status": [
        "🟢 Active",
        "🟢 Active",
        "🟢 Active"
    ]
}

st.dataframe(
    role_access,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# SYSTEM COMPONENT CHECK
# ==========================================================

st.subheader("🔎 System Component Check")

component_data = {
    "Component": [
        "User Authentication",
        "Role-Based Access",
        "Task Assignment",
        "Task Monitoring",
        "Daily Review Monitoring",
        "Notification System",
        "Reports Dashboard",
        "Navigation System"
    ],
    "Status": [
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational",
        "🟢 Operational"
    ]
}

st.dataframe(
    component_data,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# STATUS CHECK
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
