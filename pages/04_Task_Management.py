import streamlit as st

from core.navigation import require_login

from services.task_service import TaskService

st.set_page_config(

    page_title="Task Management",
    page_icon="📋",
    layout="wide"

)

require_login(["Developer","Admin"])

st.title("📋 Task Management")

st.divider()

tasks = TaskService.get_all_tasks()

if tasks is None:

    tasks = []

stats = TaskService.statistics()

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(

        "Total Tasks",

        stats["total"]

    )

with c2:

    st.metric(

        "Active",

        stats["active"]

    )

with c3:

    st.metric(

        "Inactive",

        stats["inactive"]

    )

st.divider()

tab1,tab2 = st.tabs(

    [

        "📋 Task List",

        "➕ Create Task"

    ]

)

with tab1:

    search = st.text_input(

        "Search Task"

    )

    display = tasks

    if search.strip():

        display = [

            x

            for x in tasks

            if search.lower()

            in str(x).lower()

        ]

    st.dataframe(

        display,

        use_container_width=True,

        hide_index=True

    )

with tab2:

    st.subheader("➕ Create New Task")

    task_name = st.text_input(
        "Task Name"
    )

    category = st.selectbox(
        "Category",
        [
            "Reporting",
            "Review",
            "Survey",
            "Field Visit",
            "Meeting",
            "Training",
            "Other"
        ]
    )

    frequency = st.selectbox(
        "Frequency",
        [
            "Daily",
            "Weekly",
            "Monthly",
            "Quarterly",
            "Yearly"
        ]
    )

    priority = st.selectbox(
        "Priority",
        [
            "High",
            "Medium",
            "Low"
        ]
    )

    task_link = st.text_input(
        "Task Link (Optional)"
    )

    remarks = st.text_area(
        "Remarks"
    )

    if st.button(
        "✅ Create Task",
        use_container_width=True
    ):

        status, message = TaskService.create_task(

            task_name=task_name,
            category=category,
            frequency=frequency,
            priority=priority,
            task_link=task_link,
            remarks=remarks

        )

        if status:

            st.success(message)

            st.rerun()

        else:

            st.error(message)


st.divider()

st.subheader("📋 Existing Tasks")

if len(tasks) == 0:

    st.info("No Task Found.")

else:

    st.dataframe(

        tasks,

        use_container_width=True,

        hide_index=True

    )


st.divider()

st.caption(
    "MSU / EPID Health Coordinator Monitoring System | Task Management"
)

