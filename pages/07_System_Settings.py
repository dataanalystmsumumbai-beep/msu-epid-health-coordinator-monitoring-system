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
    page_title="System Settings",
    page_icon="⚙️",
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

st.title("⚙️ System Settings")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.subheader("🖥️ System Information")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Current Role",
        current_role
    )

with c2:
    st.metric(
        "Access Level",
        "Full"
        if current_role.lower() == "developer"
        else "Operational"
    )

with c3:
    st.metric(
        "System Status",
        "🟢 Active"
    )


st.divider()


# ==========================================================
# SETTINGS TABS
# ==========================================================

tab_general, tab_permissions, tab_display = st.tabs(
    [
        "⚙️ General",
        "🔐 Permissions",
        "🎨 Display"
    ]
)


# ==========================================================
# GENERAL SETTINGS
# ==========================================================

with tab_general:

    st.subheader(
        "⚙️ General Settings"
    )

    st.info(
        "These settings control the general behaviour of the portal."
    )

    portal_name = st.text_input(
        "Portal Name",
        value="Coordinator Monitoring & Task Management System",
        key="portal_name"
    )

    default_priority = st.selectbox(
        "Default Task Priority",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        index=1,
        key="default_priority"
    )

    default_status = st.selectbox(
        "Default Task Status",
        [
            "Pending",
            "In Progress",
            "Completed"
        ],
        index=0,
        key="default_task_status"
    )

    enable_notifications = st.toggle(
        "Enable Notifications",
        value=True,
        key="enable_notifications"
    )

    enable_daily_review = st.toggle(
        "Enable Daily Review",
        value=True,
        key="enable_daily_review"
    )

    if st.button(
        "💾 Save General Settings",
        type="primary",
        use_container_width=True,
        key="save_general_settings"
    ):

        st.success(
            "General settings saved for this session."
        )


# ==========================================================
# PERMISSIONS
# ==========================================================

with tab_permissions:

    st.subheader(
        "🔐 Role Permissions"
    )


    permission_data = {

        "Permission": [

            "Manage Admin Users",
            "Manage Coordinator Users",
            "Change Admin Password",
            "Change Coordinator Password",
            "Assign Tasks",
            "Submit Daily Review",
            "Monitor Daily Reviews",
            "View System Settings"

        ],

        "Developer": [

            "✅ Yes",
            "✅ Yes",
            "✅ Yes",
            "✅ Yes",
            "✅ Yes",
            "❌ No",
            "✅ Yes",
            "✅ Yes"

        ],

        "Admin": [

            "❌ No",
            "✅ Yes",
            "❌ No",
            "✅ Yes",
            "✅ Yes",
            "❌ No",
            "✅ Yes",
            "⚠️ Limited"

        ],

        "Coordinator": [

            "❌ No",
            "❌ No",
            "❌ No",
            "❌ No",
            "❌ No",
            "✅ Yes",
            "❌ No",
            "❌ No"

        ]
    }


    st.table(
        permission_data
    )


    st.divider()


    if current_role.lower() == "developer":

        st.success(
            """
            Developer has full system-management access.
            """
        )

    else:

        st.info(
            """
            Admin has operational-management access.
            Developer-only system controls are restricted.
            """
        )


# ==========================================================
# DISPLAY
# ==========================================================

with tab_display:

    st.subheader(
        "🎨 Display Settings"
    )

    compact_mode = st.toggle(
        "Compact Dashboard Mode",
        value=False,
        key="compact_mode"
    )

    show_help_text = st.toggle(
        "Show Help Text",
        value=True,
        key="show_help_text"
    )

    show_status_icons = st.toggle(
        "Show Status Icons",
        value=True,
        key="show_status_icons"
    )

    if st.button(
        "💾 Save Display Settings",
        type="primary",
        use_container_width=True,
        key="save_display_settings"
    ):

        st.success(
            "Display settings saved for this session."
        )


st.divider()


# ==========================================================
# DEVELOPER SYSTEM CONTROLS
# ==========================================================

if current_role.lower() == "developer":

    st.subheader(
        "🛠️ Developer Controls"
    )

    st.warning(
        "These controls are intended only for the system Developer."
    )

    clear_cache = st.button(
        "🧹 Clear Application Cache",
        use_container_width=True,
        key="clear_application_cache"
    )

    if clear_cache:

        st.cache_data.clear()
        st.cache_resource.clear()

        st.success(
            "Application cache cleared successfully."
        )

        st.rerun()


    st.divider()


    st.subheader(
        "🔄 Application Refresh"
    )

    if st.button(
        "🔄 Refresh Application",
        use_container_width=True,
        key="refresh_application"
    ):

        st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "System Settings • Coordinator Monitoring & Task Management System"
)
