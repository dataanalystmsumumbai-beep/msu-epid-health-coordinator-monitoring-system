import streamlit as st

from core.navigation import require_login
from core.session import logout
from services.user_service import UserService


# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="Developer Dashboard",
    page_icon="👨‍💻",
    layout="wide"
)

require_login("Developer")


# ------------------------------------------------
# Hide Default Navigation
# ------------------------------------------------

st.markdown("""
<style>

section[data-testid="stSidebarNav"]{
    display:none;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# Load Users
# ------------------------------------------------

users = UserService.get_all_users()

if users is None:
    users = []


# ------------------------------------------------
# Sidebar
# ------------------------------------------------

with st.sidebar:

    st.markdown("# 👨‍💻 Developer")

    st.success("🟢 Online")

    st.write(
        f"**User :** {st.session_state.get('username','')}"
    )

    st.write(
        f"**Role :** {st.session_state.get('role','')}"
    )

    st.divider()

    st.markdown("### Quick Menu")

    st.write("🏠 Dashboard")
    st.write("👥 User Management")
    st.write("📊 Statistics")
    st.write("📝 Audit Logs")
    st.write("⚙️ Settings")

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.stop()


# ------------------------------------------------
# Header
# ------------------------------------------------

st.title(
    "🏥 MSU / EPID Health Coordinator Monitoring System"
)

st.caption(
    "Developer Control Panel"
)

st.divider()


# ------------------------------------------------
# Statistics
# ------------------------------------------------

total_users = len(users)

developer_count = sum(
    1
    for u in users
    if str(u.get("Role", "")) == "Developer"
)

admin_count = sum(
    1
    for u in users
    if str(u.get("Role", "")) == "Admin"
)

coordinator_count = sum(
    1
    for u in users
    if str(u.get("Role", "")) == "Coordinator"
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


dashboard_tab, create_tab, users_tab = st.tabs(
    [
        "📊 Dashboard",
        "➕ Create User",
        "👥 User List"
    ]# ------------------------------------------------
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

    username = st.text_input(
        "Username"
    )

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

    full_name = st.text_input(
        "Full Name"
    )

    designation = st.text_input(
        "Designation"
    )

    mobile = st.text_input(
        "Mobile Number"
    )

    email = st.text_input(
        "Email"
    )

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
            created_by=st.session_state.get(
                "username",
                "SYSTEM"
            )
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

    search = st.text_input(
        "🔍 Search User"
    )

    filtered_users = users

    if search.strip():

        search_text = search.strip().lower()

        filtered_users = [

            user

            for user in users

            if
            search_text in str(user.get("Username", "")).lower()
            or search_text in str(user.get("Full_Name", "")).lower()
            or search_text in str(user.get("Role", "")).lower()
            or search_text in str(user.get("Designation", "")).lower()
            or search_text in str(user.get("Mobile", "")).lower()
            or search_text in str(user.get("Email", "")).lower()

        ]

    st.dataframe(
        filtered_users,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Displayed Users",
            len(filtered_users)
        )

    with c2:

        st.metric(
            "Total Users",
            len(users)
        )

    with c3:

        active_users = len(
            [
                u
                for u in users
                if str(
                    u.get("Status", "")
                ).upper() == "ACTIVE"
            ]
        )

        st.metric(
            "Active Users",
            active_users
        )

# ------------------------------------------------
# Footer
# ------------------------------------------------

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | Developer Panel v1.0"
)
)

