import streamlit as st
import pandas as pd
from datetime import date

from config.config import (
    ROLE_COORDINATOR,
    TASK_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW
)

from utils.google_sheet import read_all

from services.task_assignment_service import (
    TaskAssignmentService
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Coordinator Dashboard",
    page_icon="👨‍⚕️",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error(
        "Please login first."
    )

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


current_user_id = str(
    current_user.get(
        "Coordinator_ID",
        current_user.get(
            "User_ID",
            ""
        )
    )
).strip()


current_username = str(
    current_user.get(
        "Username",
        ""
    )
).strip()


# ==========================================================
# ACCESS CONTROL
# ==========================================================

if current_role != ROLE_COORDINATOR:

    st.error(
        "Coordinator access required."
    )

    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "👨‍⚕️ Coordinator Dashboard"
)

st.caption(
    f"Welcome, {current_username}"
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

tasks = safe_read(
    TASK_MASTER
)

reviews = safe_read(
    DAILY_REVIEW
)


try:

    assignments = (
        TaskAssignmentService
        .get_all_assignments()
    )

except Exception:

    assignments = []


if not assignments:

    assignments = []


# ==========================================================
# MY ASSIGNMENTS
# ==========================================================

my_assignments = [

    assignment

    for assignment in assignments

    if str(
        assignment.get(
            "Coordinator_ID",
            ""
        )
    ).strip()
    == current_user_id

    and str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()

    not in [
        "removed",
        "deleted",
        "inactive"
    ]

]


# ==========================================================
# TASK LOOKUP
# ==========================================================

task_lookup = {}


for task in tasks:

    task_id = str(
        task.get(
            "Task_ID",
            ""
        )
    ).strip()


    if task_id:

        task_lookup[
            task_id
        ] = task


# ==========================================================
# TASK STATUS
# ==========================================================

total_tasks = len(
    my_assignments
)


completed_tasks = sum(

    1

    for assignment in my_assignments

    if str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "completed"

)


pending_tasks = sum(

    1

    for assignment in my_assignments

    if str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()
    == "pending"

)


in_progress_tasks = sum(

    1

    for assignment in my_assignments

    if str(
        assignment.get(
            "Status",
            ""
        )
    ).strip().lower()
    in [
        "in progress",
        "in_progress"
    ]

)


completion_percentage = (

    completed_tasks
    / total_tasks
    * 100

    if total_tasks > 0

    else 0

)


# ==========================================================
# DAILY REVIEWS
# ==========================================================

my_reviews = [

    review

    for review in reviews

    if str(
        review.get(
            "Username",
            review.get(
                "Coordinator_ID",
                review.get(
                    "Coordinator_Id",
                    ""
                )
            )
        )
    ).strip()
    in [
        current_user_id,
        current_username
    ]

]


# ==========================================================
# TOP METRICS
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "📋 Assigned",
        total_tasks
    )


with c2:

    st.metric(
        "✅ Completed",
        completed_tasks
    )


with c3:

    st.metric(
        "⏳ Pending",
        pending_tasks
    )


with c4:

    st.metric(
        "🔄 In Progress",
        in_progress_tasks
    )


with c5:

    st.metric(
        "📈 Completion",
        f"{completion_percentage:.0f}%"
    )


st.divider()


# ==========================================================
# OVERALL PROGRESS
# ==========================================================

st.subheader(
    "📊 Overall Task Progress"
)


st.progress(
    completion_percentage / 100
)


st.caption(
    f"{completion_percentage:.1f}% "
    "of assigned tasks completed"
)


st.divider()


# ==========================================================
# ASSIGNED TASKS
# ==========================================================

st.subheader(
    "📋 My Assigned Tasks"
)


if not my_assignments:

    st.info(
        "No tasks have been assigned to you."
    )

else:

    task_rows = []


    for assignment in my_assignments:

        task_id = str(
            assignment.get(
                "Task_ID",
                ""
            )
        ).strip()


        task = task_lookup.get(
            task_id,
            {}
        )


        task_name = str(
            task.get(
                "Task_Name",
                task.get(
                    "Task",
                    task_id
                )
            )
        ).strip()


        status = str(
            assignment.get(
                "Status",
                "Pending"
            )
        ).strip()


        task_rows.append(

            {
                "Assignment ID":
                    assignment.get(
                        "Assignment_ID",
                        ""
                    ),

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
                    status,

                "Remarks":
                    assignment.get(
                        "Remarks",
                        ""
                    )
            }

        )


    task_df = pd.DataFrame(
        task_rows
    )


    st.dataframe(
        task_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================================
# QUICK DAILY REVIEW
# ==========================================================

st.subheader(
    "📝 Submit Daily Review"
)


if not my_assignments:

    st.info(
        "You need an assigned task before submitting a Daily Review."
    )

else:

    task_options = {}


    for assignment in my_assignments:

        task_id = str(
            assignment.get(
                "Task_ID",
                ""
            )
        ).strip()


        task = task_lookup.get(
            task_id,
            {}
        )


        task_name = str(
            task.get(
                "Task_Name",
                task.get(
                    "Task",
                    task_id
                )
            )
        ).strip()


        assignment_id = str(
            assignment.get(
                "Assignment_ID",
                ""
            )
        ).strip()


        task_options[
            f"{task_name} ({assignment_id})"
        ] = assignment


    selected_label = st.selectbox(

        "Select Task",

        list(
            task_options.keys()
        ),

        key="dashboard_review_task"

    )


    selected_assignment = task_options[
        selected_label
    ]


    selected_task_id = str(
        selected_assignment.get(
            "Task_ID",
            ""
        )
    ).strip()


    review_date = st.date_input(

        "Review Date",

        value=date.today(),

        key="dashboard_review_date"

    )


    review_status = st.selectbox(

        "Status",

        [
            "Completed",
            "In Progress",
            "Pending"
        ],

        key="dashboard_review_status"

    )


    review_remarks = st.text_area(

        "Progress / Remarks",

        placeholder=(
            "Enter today's progress, "
            "work completed or pending reason."
        ),

        height=120,

        key="dashboard_review_remarks"

    )


    if st.button(

        "✅ Submit Daily Review",

        type="primary",

        use_container_width=True,

        key="dashboard_submit_review"

    ):

        # --------------------------------------------------
        # DUPLICATE CHECK
        # --------------------------------------------------

        duplicate = False


        for review in reviews:

            review_coordinator = str(

                review.get(
                    "Coordinator_ID",
                    review.get(
                        "Coordinator_Id",
                        review.get(
                            "Username",
                            ""
                        )
                    )
                )

            ).strip()


            review_task_id = str(

                review.get(
                    "Task_ID",
                    review.get(
                        "Task_Id",
                        ""
                    )
                )

            ).strip()


            review_date_value = str(

                review.get(
                    "Review_Date",
                    review.get(
                        "Date",
                        ""
                    )
                )

            ).strip()


            if (

                review_coordinator
                in [
                    current_user_id,
                    current_username
                ]

                and

                review_task_id
                == selected_task_id

                and

                review_date_value
                == review_date.strftime(
                    "%d-%m-%Y"
                )

            ):

                duplicate = True

                break


        if duplicate:

            st.error(
                "Daily Review for this task and date "
                "has already been submitted."
            )

        else:

            try:

                from datetime import datetime

                review_id = (
                    "REV-"
                    + datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    )
                )


                submitted_on = (
                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    )
                )


                assignment_id = str(

                    selected_assignment.get(
                        "Assignment_ID",
                        ""
                    )

                ).strip()


                row = [

                    review_id,

                    review_date.strftime(
                        "%d-%m-%Y"
                    ),

                    current_user_id,

                    selected_task_id,

                    assignment_id,

                    review_status,

                    review_remarks.strip(),

                    submitted_on

                ]


                from utils.google_sheet import (
                    insert_row,
                    update_value
                )


                insert_row(
                    DAILY_REVIEW,
                    row
                )


                # ------------------------------------------
                # UPDATE ASSIGNMENT STATUS
                # ------------------------------------------

                all_current_assignments = (

                    TaskAssignmentService
                    .get_all_assignments()

                )


                target_row = None


                for row_number, assignment in enumerate(

                    all_current_assignments,

                    start=2

                ):

                    existing_id = str(

                        assignment.get(
                            "Assignment_ID",
                            ""
                        )

                    ).strip()


                    if existing_id == assignment_id:

                        target_row = row_number

                        break


                if target_row:

                    update_value(

                        COORDINATOR_TASK_MAP,

                        target_row,

                        8,

                        review_status

                    )


                st.success(
                    "✅ Daily Review submitted successfully."
                )


                st.rerun()


            except Exception as e:

                st.error(
                    f"Unable to submit Daily Review: {e}"
                )


st.divider()


# ==========================================================
# MY REVIEW HISTORY
# ==========================================================

st.subheader(
    "📚 My Review History"
)


if my_reviews:

    st.dataframe(
        my_reviews,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No Daily Reviews submitted yet."
    )


st.divider()


# ==========================================================
# NAVIGATION
# ==========================================================

st.subheader(
    "⚡ Quick Actions"
)


q1, q2 = st.columns(2)


with q1:

    if st.button(
        "📋 Task Management",
        use_container_width=True
    ):

        st.switch_page(
            "pages/04_Task_Management.py"
        )


with q2:

    if st.button(
        "📝 Daily Review",
        use_container_width=True
    ):

        st.switch_page(
            "pages/03_Daily_Review.py"
        )
