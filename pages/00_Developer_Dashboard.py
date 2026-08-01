import streamlit as st

from core.navigation import require_login

from services.user_service import UserService
from core.session import logout

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Developer Dashboard",
    page_icon="👨‍💻",
    layout="wide"
)

require_login("Developer")

st.markdown("""
<style>
section[data-testid="stSidebarNav"]{
    display:none;
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------------
# Login Check
# ------------------------------------------------

if (
    not st.session_state.get("logged_in", False)
    or st.session_state.get("role") != "Developer"
):
    st.warning("Please login first.")
    st.switch_page("app.py")
    st.stop()
# ------------------------------------------------
# Load Users
# ------------------------------------------------

users = UserService.get_all_users()

# ------------------------------------------------
# Sidebar
# ------------------------------------------------

with st.sidebar:

    st.markdown("# 👨‍💻 Developer")

    username = st.session_state.get("username", "Guest")
    role = st.session_state.get("role", "Developer")

    st.success("🟢 Online")

    st.write(f"**User :** {username}")
    st.write(f"**Role :** {role}")

    st.divider()

    st.markdown("### Quick Menu")

    st.write("📊 Dashboard")
    st.write("👤 User Management")
    st.write("📝 Audit Logs")
    st.write("⚙️ System Settings")

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.session_state.clear()

        st.switch_page("app.py")

        st.stop()

# ------------------------------------------------
# Header
# ------------------------------------------------

st.title("🏥 MSU / EPID Health Coordinator Monitoring System")

st.caption("Developer Control Panel")

st.divider()

st.write("DEBUG SESSION")

st.json(dict(st.session_state))

# ------------------------------------------------
# Dashboard Cards
# ------------------------------------------------


total_users = len(users)

developer_count = len(
    [u for u in users if u["Role"] == "Developer"]
)

admin_count = len(
    [u for u in users if u["Role"] == "Admin"]
)

coordinator_count = len(
    [u for u in users if u["Role"] == "Coordinator"]
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👥 Total Users",
        total_users
    )

with c2:
    st.metric(
        "👨‍💻 Developers",
        developer_count
    )

with c3:
    st.metric(
        "👨‍💼 Admins",
        admin_count
    )

with c4:
    st.metric(
        "🧑‍⚕️ Coordinators",
        coordinator_count
    )

st.divider()

# ------------------------------------------------
# Tabs
# ------------------------------------------------

dashboard_tab, create_tab, users_tab = st.tabs(
    [
        "📊 Dashboard",
        "➕ Create User",
        "👥 User List"
    ]
)

# ------------------------------------------------
# Dashboard
# ------------------------------------------------

with dashboard_tab:

    st.success("✅ System Running Successfully")

    st.dataframe(
        users,
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------------
# Create User
# ------------------------------------------------

with create_tab:

    st.subheader("Create New User")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    role = st.selectbox(
        "Role",
        [
            "Developer",
            "Admin",
            "Coordinator"
        ]
    )

    full_name = st.text_input("Full Name")

    designation = st.text_input("Designation")

    mobile = st.text_input("Mobile")

    email = st.text_input("Email")

    if st.button(
        "✅ Create User",
        use_container_width=True
    ):

        status, message = UserService.create_user(
            username=username,
            password=password,
            role=role,
            full_name=full_name,
            designation=designation,
            mobile=mobile,
            email=email,
            created_by=st.session_state.username
        )

        if status:

            st.success(message)

            st.rerun()

        else:

            st.error(message)

# ------------------------------------------------
# User List
# ------------------------------------------------

with users_tab:

    st.subheader("Existing Users")

    search = st.text_input("🔍 Search User")

    if search:

        filtered = [
            u for u in users
            if search.lower() in str(u).lower()
        ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.dataframe(
            users,
            use_container_width=True,
            hide_index=True
        )
st.write("Logged In =", st.session_state.get("logged_in"))
