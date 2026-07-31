import streamlit as st

from core.navigation import require_login
from services.task_service import TaskService

# -----------------------------------
# Login Check
# -----------------------------------

require_login(["Developer", "Admin"])

# -----------------------------------
# Page
# -----------------------------------

st.set_page_config(
    page_title="Task Management",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Task Master")

st.divider()

# -----------------------------------
# Dashboard
# -----------------------------------

stats = TaskService.statistics()

c1, c2, c3 = st.columns(3)

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

tab1, tab2 = st.tabs(

    [

        "➕ Create Task",

        "📋 View Tasks"

    ]

)

# ===================================
# Create Task
# ===================================

with tab1:

    with st.form("task_form"):

        task_name = st.text_input(
            "Task Name"
        )

        category = st.text_input(
            "Category"
        )

        frequency = st.selectbox(

            "Frequency",

            [

                "Daily",

                "Weekly",

                "Monthly"

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
            "Task Link"
        )

        remarks = st.text_area(
            "Remarks"
        )

        submit = st.form_submit_button(
            "Create Task"
        )

        if submit:

            status, msg = TaskService.create_task(

                task_name,

                category,

                frequency,

                priority,

                task_link,

                remarks

            )

            if status:

                st.success(msg)

                st.rerun()

            else:

                st.error(msg)

# ===================================
# Task List
# ===================================

with tab2:

    tasks = TaskService.get_all_tasks()

    if len(tasks) == 0:

        st.info("No Tasks Found")

    else:

        st.dataframe(

            tasks,

            use_container_width=True,

            hide_index=True

        )
