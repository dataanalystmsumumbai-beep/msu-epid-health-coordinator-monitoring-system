import streamlit as st

from core.navigation import require_login
from core.session import logout

from services.user_service import UserService

# ==========================================================
# Security
# ==========================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

require_login("Admin")

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("👨‍💼 Admin Panel")

    st.success("🟢 Logged In")

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

    st.markdown("### Navigation")

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

# ==========================================================
# Header
# ==========================================================

st.title("🏥 Admin Dashboard")

st.caption("MSU / EPID Health Coordinator Monitoring System")

st.divider()

# ==========================================================
# Statistics
# ==========================================================

users = UserService.get_all_users()

developers = len(
    [
        u for u in users
        if u["Role"] == "Developer"
    ]
)

admins = len(
    [
        u for u in users
        if u["Role"] == "Admin"
    ]
)

coordinators = len(
    [
        u for u in users
        if u["Role"] == "Coordinator"
    ]
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "👥 Total Users",
        len(users)
    )

with c2:

    st.metric(
        "👨‍💻 Developers",
        developers
    )

with c3:

    st.metric(
        "👨‍💼 Admins",
        admins
    )

with c4:

    st.metric(
        "🧑‍⚕️ Coordinators",
        coordinators
    )

st.divider()

# ==========================================================
# Tabs
# ==========================================================

tab1, tab2, tab3 = st.tabs(

    [

        "📊 Dashboard",

        "👨‍⚕️ Coordinators",

        "📋 Reports"

    ]

)

# ==========================================================
# Dashboard
# ==========================================================

with tab1:

    st.success("System Running Successfully")

    st.dataframe(

        users,

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# Coordinators
# ==========================================================

with tab2:

    coordinator_list = [

        u for u in users

        if u["Role"] == "Coordinator"

    ]

    st.subheader("Coordinator List")

    st.dataframe(

        coordinator_list,

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# Reports
# ==========================================================

with tab3:

    st.info("Reports Module Coming Next")

    st.button(

        "📥 Export Excel",

        use_container_width=True

    )

    st.button(

        "📄 Export PDF",

        use_container_width=True

    )
