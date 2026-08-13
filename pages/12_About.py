import streamlit as st

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
    page_title="About System",
    page_icon="ℹ️",
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

st.title("ℹ️ About the System")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# SYSTEM INTRODUCTION
# ==========================================================

st.subheader(
    "📊 Coordinator Monitoring & Task Management System"
)

st.markdown(
    """
    This portal is designed to provide a centralised system for:

    - 👥 User management
    - 📋 Task assignment
    - 👨‍⚕️ Coordinator monitoring
    - 📝 Daily Review submission
    - 🔔 Notifications
    - 📊 Reports and dashboards
    - 🔐 Role-based access control

    The system helps management monitor assigned work,
    progress and completion through a structured workflow.
    """
)


st.divider()


# ==========================================================
# SYSTEM WORKFLOW
# ==========================================================

st.subheader(
    "🔄 System Workflow"
)

workflow = {
    "Step": [
        "1",
        "2",
        "3",
        "4",
        "5"
    ],
    "Process": [
        "User Management",
        "Task Assignment",
        "Task Execution",
        "Daily Review Submission",
        "Monitoring & Reporting"
    ],
    "Responsible": [
        "Developer / Admin",
        "Developer / Admin",
        "Coordinator",
        "Coordinator",
        "Developer / Admin"
    ]
}

st.table(
    workflow
)


st.divider()


# ==========================================================
# ROLE STRUCTURE
# ==========================================================

st.subheader(
    "👥 Role Structure"
)

role_data = {
    "Role": [
        "Developer",
        "Admin",
        "Coordinator"
    ],
    "Primary Responsibility": [
        "System and user administration",
        "Operational and Coordinator management",
        "Task execution and Daily Review"
    ]
}

st.table(
    role_data
)


st.divider()


# ==========================================================
# MAIN MODULES
# ==========================================================

st.subheader(
    "📦 Main Modules"
)

modules = [
    (
        "🔐 Authentication",
        "Secure role-based login and access control."
    ),
    (
        "👥 User Management",
        "Manage authorised system users."
    ),
    (
        "📋 Task Management",
        "Create and assign work to Coordinators."
    ),
    (
        "📝 Daily Review",
        "Capture daily task progress and status."
    ),
    (
        "🔔 Notifications",
        "Display pending, priority and review alerts."
    ),
    (
        "📊 Reports Dashboard",
        "Monitor task and review performance."
    ),
    (
        "🆘 Help Center",
        "Provide quick operational guidance."
    ),
    (
        "📖 System Manual",
        "Provide detailed system instructions."
    )
]

for module_name, description in modules:

    with st.container(border=True):

        st.markdown(
            f"### {module_name}"
        )

        st.write(
            description
        )


st.divider()


# ==========================================================
# ACCESS MODEL
# ==========================================================

st.subheader(
    "🔐 Access Model"
)

st.markdown(
    """
    ### Developer

    Full system-management access.

    ### Admin

    Operational-management access with Coordinator management.

    ### Coordinator

    Task execution and Daily Review submission access.
    """
)


st.divider()


# ==========================================================
# CURRENT USER
# ==========================================================

st.subheader(
    "👤 Current User"
)

user_info = {
    "Parameter": [
        "Username",
        "Role",
        "Login Status"
    ],
    "Value": [
        current_username,
        current_role,
        "🟢 Active"
    ]
}

st.table(
    user_info
)


st.divider()


# ==========================================================
# SYSTEM PRINCIPLES
# ==========================================================

st.subheader(
    "🎯 System Principles"
)

st.markdown(
    """
    - **Accountability** — Every assigned task has a responsible Coordinator.
    - **Transparency** — Task progress is visible through reviews and dashboards.
    - **Timeliness** — Due dates and pending work can be monitored.
    - **Role Security** — Users see only the functions permitted for their role.
    - **Centralised Monitoring** — Tasks and Daily Reviews are monitored from one portal.
    """
)


st.divider()


# ==========================================================
# FOOTER
# ==========================================================

st.success(
    "🟢 System is ready for operational use."
)

st.caption(
    "Coordinator Monitoring & Task Management System"
)
