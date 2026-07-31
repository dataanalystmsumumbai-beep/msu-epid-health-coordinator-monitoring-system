import streamlit as st

from core.navigation import require_login
from core.session import logout

from services.task_service import TaskService
from services.user_service import UserService

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Task Management",
    page_icon="📋",
    layout="wide"
)

# ==========================================================
# Login Protection
# ==========================================================

require_login(["Developer", "Admin"])

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.title("📋 Task Management")

    st.success("🟢 Logged In")

    st.write(
        f"**User :** {st.session_state.get('full_name','')}"
    )

    st.write(
        f"**Role :** {st.session_state.get('role','')}"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()

# ==========================================================
# Header
# ==========================================================

st.title("📋 Task Management")

st.caption("MSU / EPID Health Coordinator Monitoring System")

st.divider()

# ==========================================================
# Statistics
# ==========================================================

stats = TaskService.statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📋 Total Tasks",
        stats["total"]
    )

with c2:
    st.metric(
        "⏳ Pending",
        stats["pending"]
    )

with c3:
    st.metric(
        "✅ Completed",
        stats["completed"]
    )

with c4:
    st.metric(
        "📈 Progress",
        f'{stats["progress"]}%'
    )

st.divider()

# ==========================================================
# Tabs
# ==========================================================

tab1, tab2 = st.tabs(
    [
        "➕ Create Task",
        "📋 Task List"
    ]
)

# ==========================================================
# Create Task
# ==========================================================

with tab1:

    st.subheader("Create New Task")

    coordinators = [
        u["Username"]
        for u in UserService.get_all_users()
        if u["Role"] == "Coordinator"
    ]

    with st.form("create_task_form"):

        task_name = st.text_input("Task Name")

        description = st.text_area("Description")

        assigned_to = st.selectbox(
            "Assign Coordinator",
            coordinators if coordinators else ["No Coordinator"]
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        due_date = st.date_input("Due Date")

        submit = st.form_submit_button(
            "✅ Create Task",
            use_container_width=True
        )

        if submit:

            status, message = TaskService.create_task(
                task_name=task_name,
                description=description,
                assigned_to=assigned_to,
                priority=priority,
                due_date=str(due_date),
                created_by=st.session_state.username
            )

            if status:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
              # ==========================================================
# Task List
# ==========================================================

with tab2:

    st.subheader("📋 Task List")

    tasks = TaskService.get_all_tasks()

    if len(tasks) == 0:

        st.info("No Tasks Available")

    else:

        c1, c2, c3 = st.columns(3)

        with c1:
            search = st.text_input(
                "🔍 Search Task"
            )

        with c2:

            status_filter = st.selectbox(

                "Status",

                [

                    "All",

                    "Pending",

                    "In Progress",

                    "Completed"

                ]

            )

        with c3:

            priority_filter = st.selectbox(

                "Priority",

                [

                    "All",

                    "High",

                    "Medium",

                    "Low"

                ]

            )

        filtered = []

        for task in tasks:

            if (

                search

                and

                search.lower()

                not in str(task).lower()

            ):

                continue

            if (

                status_filter != "All"

                and

                task["Status"] != status_filter

            ):

                continue

            if (

                priority_filter != "All"

                and

                task["Priority"] != priority_filter

            ):

                continue

            filtered.append(task)

        st.write(
            f"**Total Records : {len(filtered)}**"
        )

        st.dataframe(

            filtered,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        st.subheader("Task Summary")

        total = len(filtered)

        completed = len(

            [

                x

                for x in filtered

                if x["Status"] == "Completed"

            ]

        )

        pending = len(

            [

                x

                for x in filtered

                if x["Status"] == "Pending"

            ]

        )

        progress = len(

            [

                x

                for x in filtered

                if x["Status"] == "In Progress"

            ]

        )

        a, b, c = st.columns(3)

        with a:

            st.metric(

                "Completed",

                completed

            )

        with b:

            st.metric(

                "Pending",

                pending

            )

        with c:

            st.metric(

                "In Progress",

                progress

            )
          # ==========================================================
# Update Task
# ==========================================================

st.divider()

st.subheader("✏ Update Task")

if len(filtered) == 0:

    st.info("No Task Available")

else:

    task_options = {

        f"{t['Task_ID']} | {t['Task_Name']}": t

        for t in filtered

    }

    selected = st.selectbox(

        "Select Task",

        list(task_options.keys())

    )

    task = task_options[selected]

    with st.form("update_task"):

        new_status = st.selectbox(

            "Status",

            [

                "Pending",

                "In Progress",

                "Completed"

            ],

            index=[

                "Pending",

                "In Progress",

                "Completed"

            ].index(task["Status"])

            if task["Status"] in

            [

                "Pending",

                "In Progress",

                "Completed"

            ]

            else 0

        )

        remarks = st.text_area(

            "Remarks",

            value=task.get("Remarks", "")

        )

        save = st.form_submit_button(

            "💾 Update Task",

            use_container_width=True

        )

        if save:

            row_number = tasks.index(task) + 2

            TaskService.update_status(

                row_number,

                new_status

            )

            TaskService.update_remarks(

                row_number,

                remarks

            )

            st.success(

                "Task Updated Successfully"

            )

            st.rerun()
