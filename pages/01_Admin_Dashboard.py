import streamlit as st

from core.navigation import require_login
from core.session import logout

from services.user_service import UserService

from services.task_service import TaskService
from services.task_assignment_service import TaskAssignmentService
from datetime import date


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

dashboard_tab, coordinator_tab, assignment_tab, report_tab = st.tabs(
    [
        "📊 Dashboard",
        "👨‍⚕️ Coordinators",
        "📋 Task Assignment",
        "📈 Reports"
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
# Task Assignment
# ==========================================================

with assignment_tab:

    st.subheader("📋 Assign Task")

    coordinators = [

        u

        for u in users

        if str(u.get("Role", "")).strip() == "Coordinator"

    ]

    tasks = TaskService.get_all_tasks()

    if len(coordinators) == 0:

        st.warning("No Coordinator Available.")

    elif len(tasks) == 0:

        st.warning("No Task Available.")

    else:

        coordinator_names = {

            f"{c.get('Full_Name')} ({c.get('Username')})": c.get("User_ID")

            for c in coordinators

        }

        task_names = {

            t.get("Task_Name"): t.get("Task_ID")

            for t in tasks

        }

        coordinator = st.selectbox(

            "Coordinator",

            list(coordinator_names.keys())

        )

        task = st.selectbox(

            "Task",

            list(task_names.keys())

        )

        priority = st.selectbox(

            "Priority",

            [

                "High",

                "Medium",

                "Low"

            ]

        )

        assigned_date = st.date_input(

            "Assigned Date",

            value=date.today()

        )

        due_date = st.date_input(

            "Due Date",

            value=date.today()

        )

        remarks = st.text_area(

            "Remarks"

        )

        if st.button(

            "✅ Assign Task",

            use_container_width=True

        ):

            status, message = TaskAssignmentService.assign_task(

                coordinator_id=coordinator_names[coordinator],

                task_id=task_names[task],

                assigned_by=st.session_state.get("username"),

                assigned_date=str(assigned_date),

                due_date=str(due_date),

                priority=priority,

                remarks=remarks

            )

            if status:

                st.success(message)

            else:

                st.error(message)



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
