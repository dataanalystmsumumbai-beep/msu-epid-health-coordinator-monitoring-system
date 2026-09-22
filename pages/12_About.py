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

st.title("ℹ️ About the System")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# SYSTEM OVERVIEW
# ==========================================================

st.subheader(
    "📊 Coordinator Monitoring & Task Management System"
)

st.markdown(
    """
    The **Coordinator Monitoring & Task Management System** is a
    centralised web-based monitoring portal designed to support
    structured task assignment, Coordinator monitoring, Daily Review
    tracking, notifications and management reporting.

    The system provides role-based access so that different users can
    access the functions relevant to their responsibilities.
    """
)


# ==========================================================
# KEY FUNCTIONS
# ==========================================================

st.subheader("🎯 Key Functions")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 👥")
    st.markdown("**User Management**")
    st.caption(
        "Manage authorised users and system access."
    )

with c2:
    st.markdown("### 📋")
    st.markdown("**Task Management**")
    st.caption(
        "Create, assign and monitor Coordinator tasks."
    )

with c3:
    st.markdown("### 📝")
    st.markdown("**Daily Review**")
    st.caption(
        "Record and monitor daily task progress."
    )

with c4:
    st.markdown("### 📊")
    st.markdown("**Reporting**")
    st.caption(
        "Monitor task and review performance."
    )


st.divider()


# ==========================================================
# SYSTEM WORKFLOW
# ==========================================================

st.subheader("🔄 System Workflow")

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

st.dataframe(
    workflow,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# ROLE STRUCTURE
# ==========================================================

st.subheader("👥 Role Structure")

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
    ],
    "Access Level": [
        "Full System Access",
        "Operational Management",
        "Task & Daily Review"
    ]
}

st.dataframe(
    role_data,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# MAIN MODULES
# ==========================================================

st.subheader("📦 Main Modules")

modules = [
    (
        "🔐 Authentication",
        "Role-based login and access control."
    ),
    (
        "👨‍💻 Developer Dashboard",
        "System-level monitoring and administration."
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
        "👨‍⚕️ Coordinator Dashboard",
        "Provide Coordinators with their assigned work."
    ),
    (
        "📝 Daily Review",
        "Capture daily task progress and review status."
    ),
    (
        "🔔 Notifications",
        "Display pending, priority and review alerts."
    ),
    (
        "📊 Reports Dashboard",
        "Monitor task and Daily Review performance."
    ),
    (
        "🆘 Help Center",
        "Provide quick operational guidance."
    ),
    (
        "⚙️ System Settings",
        "Manage available system configuration options."
    ),
    (
        "📖 System Manual",
        "Provide detailed system instructions."
    ),
    (
        "🟢 System Status",
        "Display application and module status."
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

st.subheader("🔐 Access Model")

access_model = {
    "Role": [
        "Developer",
        "Admin",
        "Coordinator"
    ],
    "Description": [
        "Full system-management and administration access.",
        "Operational-management access including Coordinator management.",
        "Task execution and Daily Review access."
    ]
}

st.dataframe(
    access_model,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# CURRENT USER
# ==========================================================

st.subheader("👤 Current User")

user_info = {
    "Parameter": [
        "Username",
        "Role",
        "User ID",
        "Login Status"
    ],
    "Value": [
        current_username if current_username else "Not Available",
        current_role if current_role else "Not Available",
        current_user_id if current_user_id else "Not Available",
        "🟢 Active"
    ]
}

st.dataframe(
    user_info,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# SYSTEM PRINCIPLES
# ==========================================================

st.subheader("🎯 System Principles")

principles = [
    (
        "Accountability",
        "Every assigned task has a responsible Coordinator."
    ),
    (
        "Transparency",
        "Task progress can be monitored through reviews and dashboards."
    ),
    (
        "Timeliness",
        "Due dates and pending work can be monitored."
    ),
    (
        "Role Security",
        "Users access functions according to their assigned role."
    ),
    (
        "Centralised Monitoring",
        "Tasks and Daily Reviews are monitored through one portal."
    )
]

for principle, description in principles:

    st.markdown(
        f"**{principle}** — {description}"
    )


st.divider()


# ==========================================================
# SYSTEM CAPABILITIES
# ==========================================================

st.subheader("🚀 System Capabilities")

capabilities = {
    "Capability": [
        "Role-Based Access",
        "Task Assignment",
        "Task Monitoring",
        "Daily Review Tracking",
        "Notification Monitoring",
        "Reports & Dashboards",
        "User Administration",
        "System Status Monitoring"
    ],
    "Availability": [
        "🟢 Available",
        "🟢 Available",
        "🟢 Available",
        "🟢 Available",
        "🟢 Available",
        "🟢 Available",
        "🟢 Available",
        "🟢 Available"
    ]
}

st.dataframe(
    capabilities,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# OPERATIONAL STATUS
# ==========================================================

st.subheader("🟢 Operational Status")

st.success(
    "The Coordinator Monitoring & Task Management System "
    "is configured for operational use."
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Coordinator Monitoring & Task Management System"
)

st.caption(
    "Role-Based Monitoring • Task Management • Daily Review • Reporting"
)
