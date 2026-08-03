import streamlit as st

from core.navigation import require_login
from core.session import logout

from services.user_service import UserService


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

require_login("Admin")


# ==========================================================
# Hide Default Navigation
# ==========================================================

st.markdown("""
<style>

section[data-testid="stSidebarNav"]{
    display:none;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# Load Data
# ==========================================================

users = UserService.get_all_users()

if users is None:
    users = []


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("👨‍💼 Admin Panel")

    st.success("🟢 Online")

    st.write(
        f"**Name :** {st.session_state.get('full_name','')}"
    )

    st.write(
        f"**Username :** {st.session_state.get('username','')}"
    )

    st.write(
        f"**Role :** {st.session_state.get('role','')}"
    )

    st.divider()

    st.markdown("### Quick Menu")

    st.write("🏠 Dashboard")
    st.write("👨‍⚕️ Coordinators")
    st.write("📋 Tasks")
    st.write("📊 Reports")
    st.write("🔔 Notifications")

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()
        st.stop()


# ==========================================================
# Header
# ==========================================================

st.title("🏥 Admin Dashboard")

st.caption("MSU / EPID Health Coordinator Monitoring System")

st.divider()


# ==========================================================
# Statistics
# ==========================================================

total_users = len(users)

developers = sum(
    1
    for u in users
   if str(u.get("Role", "")).strip().upper() == "DEVELOPER"
)

admins = sum(
    1
    for u in users
    if str(u.get("Role","")) == "Admin"
)

coordinators = sum(
    1
    for u in users
   if str(u.get("Role", "")).strip().upper() == "COORDINATOR"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("👥 Total Users", total_users)

with c2:
    st.metric("👨‍💻 Developers", developers)

with c3:
    st.metric("👨‍💼 Admins", admins)

with c4:
    st.metric("🧑‍⚕️ Coordinators", coordinators)

st.divider()


# ==========================================================
# Tabs
# ==========================================================

dashboard_tab, coordinator_tab, report_tab = st.tabs(
    [
        "📊 Dashboard",
        "👨‍⚕️ Coordinators",
        "📋 Reports"
    ]
)


# ==========================================================
# Dashboard
# ==========================================================

with dashboard_tab:

    st.success("✅ System Running Successfully")

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# Coordinator List
# ==========================================================

with coordinator_tab:

    st.subheader("Coordinator List")

    coordinator_list = [

        u

        for u in users

       if str(u.get("Role", "")).strip().upper() == "COORDINATOR"

    ]

    st.dataframe(
        coordinator_list,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Coordinators",
        len(coordinator_list)
    )


# ==========================================================
# Reports
# ==========================================================

with report_tab:

    st.info(
        "Reports Module will be added in next update."
    )

    c1, c2 = st.columns(2)

    with c1:

        st.button(
            "📥 Export Excel",
            use_container_width=True
        )

    with c2:

        st.button(
            "📄 Export PDF",
            use_container_width=True
        )


# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | Admin Panel v1.0"
)
