import streamlit as st
import pandas as pd

from config.config import (
    ROLE_ADMIN,
    COORDINATOR_MASTER,
    TASK_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW
)

from utils.google_sheet import read_all

from core.navigation import logout_button


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error("Please login first.")
    st.stop()


# ==========================================================
# CURRENT USER
# ==========================================================

current_user = st.session_state.get(
    "user",
    {}
)

current_role = str(
    current_user.get(
        "Role",
        ""
    )
).strip()


# ==========================================================
# ACCESS CONTROL
# ==========================================================

if current_role != ROLE_ADMIN:

    st.error(
        "Admin access required."
    )

    st.stop()


logout_button()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "👨‍💼 Admin Dashboard"
)

st.caption(
    "MSU / EPID Health Coordinator Monitoring System"
)

st.divider()


# ==========================================================
# SAFE READ
# ==========================================================

def safe_read(sheet_name):

    try:

        data = read_all(
            sheet_name
        )

        return data if data else []

    except Exception:

        return []


# ==========================================================
# LOAD DATA
# ==========================================================

coordinators = safe_read(
    COORDINATOR_MASTER
)

tasks = safe_read(
    TASK_MASTER
)

assignments = safe_read(
    COORDINATOR_TASK_MAP
)

reviews = safe_read(
    DAILY_REVIEW
)


# ==========================================================
# ACTIVE RECORDS
# ==========================================================

active_coordinators = [

    x

    for x in coordinators

    if str(
        x.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()
    == "ACTIVE"

]


active_tasks = [

    x

    for x in tasks

    if str(
        x.get(
            "Status",
            "ACTIVE"
        )
    ).strip().upper()
    == "ACTIVE"

]


# ==========================================================
# ASSIGNMENT STATUS
# ==========================================================

pending_assignments = sum(

    1

    for x in assignments

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "pending"

)


in_progress_assignments = sum(

    1

    for x in assignments

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    in [
        "in progress",
        "in_progress"
    ]

)


completed_assignments = sum(

    1

    for x in assignments

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "completed"

)


# ==========================================================
# REVIEW STATUS
# ==========================================================

completed_reviews = sum(

    1

    for x in reviews

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "completed"

)


pending_reviews = sum(

    1

    for x in reviews

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "pending"

)


in_progress_reviews = sum(

    1

    for x in reviews

    if str(
        x.get(
            "Status",
            ""
        )
    ).strip().lower()
    in [
        "in progress",
        "in_progress"
    ]

)


# ==========================================================
# TOP METRICS
# ==========================================================

c1, c2, c3, c4, c5, c6 = st.columns(6)


with c1:

    st.metric(
        "👨‍⚕️ Coordinators",
        len(
            active_coordinators
        )
    )


with c2:

    st.metric(
        "📋 Active Tasks",
        len(
            active_tasks
        )
    )


with c3:

    st.metric(
        "📌 Assignments",
        len(
            assignments
        )
    )


with c4:

    st.metric(
        "⏳ Pending",
        pending_assignments
    )


with c5:

    st.metric(
        "✅ Completed",
        completed_assignments
    )


with c6:

    st.metric(
        "📝 Reviews",
        len(
            reviews
        )
    )


st.divider()


# ==========================================================
# TASK PROGRESS
# ==========================================================

st.subheader(
    "📊 Task Assignment Progress"
)


total_assignments = len(
    assignments
)


if total_assignments:

    completion_percentage = (

        completed_assignments
        / total_assignments

    )

else:

    completion_percentage = 0


st.progress(
    completion_percentage
)


st.caption(
    f"Task completion: "
    f"{completion_percentage * 100:.1f}%"
)


st.divider()


# ==========================================================
# COORDINATOR-WISE MONITORING
# ==========================================================

st.subheader(
    "👨‍⚕️ Coordinator-wise Monitoring"
)


coordinator_rows = []


for coordinator in active_coordinators:

    coordinator_id = str(
        coordinator.get(
            "Coordinator_ID",
            coordinator.get(
                "User_ID",
                ""
            )
        )
    ).strip()


    coordinator_name = str(
        coordinator.get(
            "Coordinator_Name",
            coordinator.get(
                "Full_Name",
                coordinator.get(
                    "Username",
                    coordinator_id
                )
            )
        )
    ).strip()


    coordinator_assignments = [

        x

        for x in assignments

        if str(
            x.get(
                "Coordinator_ID",
                ""
            )
        ).strip()
        == coordinator_id

    ]


    assigned = len(
        coordinator_assignments
    )


    completed = sum(

        1

        for x in coordinator_assignments

        if str(
            x.get(
                "Status",
                ""
            )
        ).strip().lower()
        == "completed"

    )


    pending = sum(

        1

        for x in coordinator_assignments

        if str(
            x.get(
                "Status",
                ""
            )
        ).strip().lower()
        == "pending"

    )


    in_progress = sum(

        1

        for x in coordinator_assignments

        if str(
            x.get(
                "Status",
                ""
            )
        ).strip().lower()
        in [
            "in progress",
            "in_progress"
        ]

    )


    completion = (

        completed
        / assigned
        * 100

        if assigned
        else 0

    )


    coordinator_rows.append(

        {
            "Coordinator": coordinator_name,
            "Assigned": assigned,
            "Completed": completed,
            "In Progress": in_progress,
            "Pending": pending,
            "Completion %": round(
                completion,
                1
            )
        }

    )


if coordinator_rows:

    coordinator_df = pd.DataFrame(
        coordinator_rows
    )

    st.dataframe(
        coordinator_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No coordinator data available."
    )


st.divider()


# ==========================================================
# DAILY REVIEW MONITORING
# ==========================================================

st.subheader(
    "📝 Daily Review Monitoring"
)


r1, r2, r3, r4 = st.columns(4)


with r1:

    st.metric(
        "Total Reviews",
        len(
            reviews
        )
    )


with r2:

    st.metric(
        "Completed",
        completed_reviews
    )


with r3:

    st.metric(
        "In Progress",
        in_progress_reviews
    )


with r4:

    st.metric(
        "Pending",
        pending_reviews
    )


if reviews:

    st.dataframe(
        reviews,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No Daily Review records available."
    )


st.divider()


# ==========================================================
# ASSIGNMENT MONITORING
# ==========================================================

st.subheader(
    "📋 Recent Task Assignments"
)


if assignments:

    assignment_rows = []


    for assignment in assignments:

        coordinator_id = str(
            assignment.get(
                "Coordinator_ID",
                ""
            )
        ).strip()


        task_id = str(
            assignment.get(
                "Task_ID",
                ""
            )
        ).strip()


        coordinator_name = coordinator_id


        for coordinator in active_coordinators:

            cid = str(
                coordinator.get(
                    "Coordinator_ID",
                    coordinator.get(
                        "User_ID",
                        ""
                    )
                )
            ).strip()


            if cid == coordinator_id:

                coordinator_name = str(
                    coordinator.get(
                        "Coordinator_Name",
                        coordinator.get(
                            "Full_Name",
                            coordinator_id
                        )
                    )
                ).strip()

                break


        task_name = task_id


        for task in active_tasks:

            tid = str(
                task.get(
                    "Task_ID",
                    ""
                )
            ).strip()


            if tid == task_id:

                task_name = str(
                    task.get(
                        "Task_Name",
                        task.get(
                            "Task",
                            task_id
                        )
                    )
                ).strip()

                break


        assignment_rows.append(

            {
                "Assignment ID":
                    assignment.get(
                        "Assignment_ID",
                        ""
                    ),

                "Coordinator":
                    coordinator_name,

                "Task":
                    task_name,

                "Assigned Date":
                    assignment.get(
                        "Assigned_Date",
                        ""
                    ),

                "Due Date":
                    assignment.get(
                        "Due_Date",
                        ""
                    ),

                "Priority":
                    assignment.get(
                        "Priority",
                        ""
                    ),

                "Status":
                    assignment.get(
                        "Status",
                        ""
                    ),

                "Remarks":
                    assignment.get(
                        "Remarks",
                        ""
                    )
            }

        )


    assignment_df = pd.DataFrame(
        assignment_rows
    )


    st.dataframe(
        assignment_df.tail(20),
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No task assignments available."
    )


st.divider()


# ==========================================================
# ADMIN QUICK ACTIONS
# ==========================================================

st.subheader(
    "⚡ Quick Actions"
)


q1, q2, q3 = st.columns(3)


with q1:

    if st.button(
        "📋 Open Task Management",
        use_container_width=True
    ):

        st.switch_page(
            "pages/04_Task_Management.py"
        )


with q2:

    if st.button(
        "📝 Open Daily Review",
        use_container_width=True
    ):

        st.switch_page(
            "pages/03_Daily_Review.py"
        )


with q3:

    if st.button(
        "👥 User Management",
        use_container_width=True
    ):

        st.switch_page(
            "pages/05_User_Management.py"
        )
