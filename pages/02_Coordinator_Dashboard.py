import streamlit as st

from core.navigation import require_login
from core.session import logout

from services.task_assignment_service import TaskAssignmentService
from services.task_service import TaskService



# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Coordinator Dashboard",
    page_icon="🩺",
    layout="wide"
)

require_login("Coordinator")

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("🩺 Coordinator")

    st.success("🟢 Logged In")

    st.write(
        f"**Name :** {st.session_state.get('full_name', '')}"
    )

    st.write(
        f"**Username :** {st.session_state.get('username', '')}"
    )

    st.write(
        f"**Role :** {st.session_state.get('role', '')}"
    )

    st.divider()

    st.markdown("### Navigation")

    st.write("🏠 Dashboard")
    st.write("📝 Daily Review")
    st.write("📋 My Tasks")
    st.write("📊 Progress")
    st.write("🔔 Notifications")

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.rerun()

# ==========================================================
# Header
# ==========================================================

st.title("🩺 Coordinator Dashboard")

st.caption("MSU / EPID Health Coordinator Monitoring System")

st.divider()

# ==========================================================
# Dashboard Cards
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📋 Assigned Tasks", "0")

with c2:
    st.metric("✅ Completed", "0")

with c3:
    st.metric("⏳ Pending", "0")

with c4:
    st.metric("📈 Progress", "0%")

st.divider()

# ==========================================================
# Tabs
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Dashboard",
        "📋 My Tasks",
        "🔔 Notifications"
    ]
)

# ==========================================================
# Dashboard Tab
# ==========================================================

with tab1:

    st.success("Welcome to Coordinator Dashboard.")

    st.info(
        "Daily Review and Task Management modules will display here."
    )

# ==========================================================
# Tasks Tab
# ==========================================================

with tab2:

    st.subheader("📋 My Assigned Tasks")

    assignments = TaskAssignmentService.coordinator_tasks(
        st.session_state.get("user_id")
    )

    if len(assignments) == 0:

        st.info("No Task Assigned.")

    else:

        tasks = TaskService.get_all_tasks()

        task_lookup = {

            t.get("Task_ID"): t.get("Task_Name")

            for t in tasks

        }

        display = []

        for a in assignments:

            display.append({

                "Task":
                    task_lookup.get(
                        a.get("Task_ID"),
                        a.get("Task_ID")
                    ),

                "Priority":
                    a.get("Priority"),

                "Assigned Date":
                    a.get("Assigned_Date"),

                "Due Date":
                    a.get("Due_Date"),

                "Status":
                    a.get("Status")

            })

        st.dataframe(

            display,

            use_container_width=True,

            hide_index=True

        )
        
# ==========================================================
# Notifications Tab
# ==========================================================

with tab3:

    st.subheader("Notifications")

    st.info("No notifications available.")

# ==========================================================
# Footer
# ==========================================================

st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | Coordinator Panel v1.0"
)
