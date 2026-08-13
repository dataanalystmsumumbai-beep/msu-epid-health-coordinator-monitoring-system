import streamlit as st
from datetime import date, datetime

from core.navigation import require_login
from services.task_assignment_service import TaskAssignmentService
from services.task_service import TaskService
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)
from config.config import (
    DAILY_REVIEW,
    COORDINATOR_TASK_MAP
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)

require_login([
    "Developer",
    "Admin",
    "Coordinator"
])


# ==========================================================
# SESSION
# ==========================================================

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()

current_role = str(
    st.session_state.get(
        "role",
        ""
    )
).strip()

current_user_id = str(
    st.session_state.get(
        "user_id",
        current_username
    )
).strip()


# ==========================================================
# HEADER
# ==========================================================

st.title("📝 Daily Review")

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# HELPER
# ==========================================================

def get_value(record, *keys):

    for key in keys:

        value = record.get(
            key,
            ""
        )

        if value is not None and str(
            value
        ).strip():

            return value

    return ""


# ==========================================================
# LOAD TASKS
# ==========================================================

try:

    all_tasks = TaskService.get_all_tasks()

except Exception:

    all_tasks = []

if all_tasks is None:

    all_tasks = []


# ==========================================================
# LOAD ASSIGNMENTS
# ==========================================================

try:

    all_assignments = (
        TaskAssignmentService
        .get_all_assignments()
    )

except Exception:

    all_assignments = []

if all_assignments is None:

    all_assignments = []


# ==========================================================
# LOAD DAILY REVIEWS
# ==========================================================

try:

    all_reviews = read_all(
        DAILY_REVIEW
    )

except Exception:

    all_reviews = []

if all_reviews is None:

    all_reviews = []


# ==========================================================
# TASK LOOKUP
# ==========================================================

task_lookup = {}

for task in all_tasks:

    task_id = str(
        get_value(
            task,
            "Task_ID",
            "Task_Id",
            "ID"
        )
    ).strip()

    if task_id:

        task_lookup[
            task_id
        ] = task


# ==========================================================
# COORDINATOR ASSIGNED TASKS
# ==========================================================

if current_role == "Coordinator":

    coordinator_assignments = [

        assignment

        for assignment in all_assignments

        if str(
            get_value(
                assignment,
                "Coordinator_ID",
                "Coordinator_Id"
            )
        ).strip()
        ==
        current_user_id

        and

        str(
            get_value(
                assignment,
                "Status"
            )
        ).strip().lower()

        not in [
            "removed",
            "inactive",
            "deleted"
        ]

    ]

else:

    coordinator_assignments = all_assignments


# ==========================================================
# BUILD TASK DISPLAY DATA
# ==========================================================

assigned_tasks = []

for assignment in coordinator_assignments:

    task_id = str(
        get_value(
            assignment,
            "Task_ID",
            "Task_Id"
        )
    ).strip()

    task = task_lookup.get(
        task_id,
        {}
    )

    task_name = get_value(
        task,
        "Task_Name",
        "Task",
        "Name"
    )

    if not task_name:

        task_name = get_value(
            assignment,
            "Task_Name",
            "Task"
        )

    assigned_tasks.append(
        {
            "assignment": assignment,
            "task": task,
            "task_id": task_id,
            "task_name": task_name
        }
    )


# ==========================================================
# COORDINATOR VIEW
# ==========================================================

if current_role == "Coordinator":

    st.subheader(
        "📋 My Assigned Tasks"
    )

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    total_tasks = len(
        assigned_tasks
    )

    completed_tasks = 0
    pending_tasks = 0
    in_progress_tasks = 0

    for item in assigned_tasks:

        assignment = item[
            "assignment"
        ]

        status = str(
            get_value(
                assignment,
                "Status"
            )
        ).strip().lower()

        if status == "completed":

            completed_tasks += 1

        elif status in [
            "in progress",
            "in_progress"
        ]:

            in_progress_tasks += 1

        else:

            pending_tasks += 1


    completion_rate = (

        (
            completed_tasks
            / total_tasks
        )
        * 100

        if total_tasks > 0

        else 0

    )


    c1, c2, c3, c4 = st.columns(4)

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
            "📈 Progress",
            f"{completion_rate:.0f}%"
        )


    st.divider()


    # ------------------------------------------------------
    # PROGRESS
    # ------------------------------------------------------

    st.progress(
        completion_rate / 100
    )

    st.caption(
        f"Overall task completion: "
        f"{completion_rate:.1f}%"
    )


    st.divider()


    # ------------------------------------------------------
    # SUBMIT DAILY REVIEW
    # ------------------------------------------------------

    st.subheader(
        "📝 Submit Daily Review"
    )

    if not assigned_tasks:

        st.info(
            "No tasks have been assigned to you."
        )

    else:

        task_options = {}

        for item in assigned_tasks:

            assignment = item[
                "assignment"
            ]

            task_id = item[
                "task_id"
            ]

            task_name = item[
                "task_name"
            ]

            due_date = get_value(
                assignment,
                "Due_Date",
                "Due Date"
            )

            label = task_name

            if due_date:

                label = (
                    f"{task_name} "
                    f"| Due: {due_date}"
                )

            task_options[
                task_id
            ] = label


        selected_task_id = st.selectbox(

            "Select Assigned Task",

            list(
                task_options.keys()
            ),

            format_func=lambda x:
            task_options.get(
                x,
                x
            ),

            key="daily_review_task"

        )


        selected_assignment = None

        selected_task = None

        for item in assigned_tasks:

            if item[
                "task_id"
            ] == selected_task_id:

                selected_assignment = (
                    item["assignment"]
                )

                selected_task = (
                    item["task"]
                )

                break


        st.markdown(
            f"**Task:** "
            f"{task_options.get(selected_task_id)}"
        )


        col1, col2 = st.columns(2)

        with col1:

            review_date = st.date_input(
                "Review Date",
                value=date.today(),
                key="review_date"
            )

        with col2:

            review_status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "In Progress",
                    "Pending"
                ],
                key="review_status"
            )


        remarks = st.text_area(

            "Remarks / Progress Update",

            placeholder=(
                "Enter today's work, "
                "progress, observations "
                "or pending reason."
            ),

            height=140,

            key="review_remarks"

        )


        submit_review = st.button(

            "✅ Submit Daily Review",

            use_container_width=True,

            key="submit_daily_review"

        )


        if submit_review:

            if not selected_task_id:

                st.error(
                    "Please select a task."
                )

            else:

                # ------------------------------------------
                # PREVENT DUPLICATE SAME-DAY SUBMISSION
                # ------------------------------------------

                duplicate = False

                for review in all_reviews:

                    review_username = str(
                        get_value(
                            review,
                            "Username",
                            "Coordinator_ID",
                            "Coordinator_Id"
                        )
                    ).strip()

                    review_task = str(
                        get_value(
                            review,
                            "Task_ID",
                            "Task_Id"
                        )
                    ).strip()

                    review_date_value = str(
                        get_value(
                            review,
                            "Review_Date",
                            "Date"
                        )
                    ).strip()

                    if (
                        review_username
                        == current_user_id

                        and

                        review_task
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
                        "Daily Review for this task "
                        "has already been submitted "
                        "for the selected date."
                    )

                else:

                    try:

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

                        assignment_id = get_value(
                            selected_assignment,
                            "Assignment_ID",
                            "Assignment_Id",
                            "ID"
                        )

                        row = [

                            review_id,

                            review_date.strftime(
                                "%d-%m-%Y"
                            ),

                            current_user_id,

                            selected_task_id,

                            assignment_id,

                            review_status,

                            remarks.strip(),

                            submitted_on

                        ]

                        insert_row(
                            DAILY_REVIEW,
                            row
                        )

                        # ----------------------------------
                        # UPDATE ASSIGNMENT STATUS
                        # ----------------------------------

                        assignment_row = None

                        for index, assignment in enumerate(
                            all_assignments,
                            start=2
                        ):

                            if (
                                str(
                                    get_value(
                                        assignment,
                                        "Assignment_ID",
                                        "Assignment_Id",
                                        "ID"
                                    )
                                ).strip()
                                == str(
                                    assignment_id
                                ).strip()
                            ):

                                assignment_row = index

                                break


                        if assignment_row:

                            update_value(

                                COORDINATOR_TASK_MAP,

                                assignment_row,

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


    # ------------------------------------------------------
    # MY REVIEW HISTORY
    # ------------------------------------------------------

    st.subheader(
        "📚 My Review History"
    )

    my_reviews = [

        review

        for review in all_reviews

        if str(
            get_value(
                review,
                "Username",
                "Coordinator_ID",
                "Coordinator_Id"
            )
        ).strip()
        ==
        current_user_id

    ]

    if not my_reviews:

        st.info(
            "No Daily Reviews submitted yet."
        )

    else:

        st.dataframe(
            my_reviews,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# ADMIN / DEVELOPER VIEW
# ==========================================================

else:

    st.subheader(
        "📊 Daily Review Monitoring"
    )

    # ------------------------------------------------------
    # METRICS
    # ------------------------------------------------------

    total_reviews = len(
        all_reviews
    )

    completed_reviews = sum(

        1

        for review in all_reviews

        if str(
            get_value(
                review,
                "Status"
            )
        ).strip().lower()
        == "completed"

    )

    pending_reviews = sum(

        1

        for review in all_reviews

        if str(
            get_value(
                review,
                "Status"
            )
        ).strip().lower()
        == "pending"

    )

    in_progress_reviews = sum(

        1

        for review in all_reviews

        if str(
            get_value(
                review,
                "Status"
            )
        ).strip().lower()
        in [
            "in progress",
            "in_progress"
        ]

    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📝 Total Reviews",
            total_reviews
        )

    with c2:

        st.metric(
            "✅ Completed",
            completed_reviews
        )

    with c3:

        st.metric(
            "⏳ Pending",
            pending_reviews
        )

    with c4:

        st.metric(
            "🔄 In Progress",
            in_progress_reviews
        )


    st.divider()


    # ------------------------------------------------------
    # REVIEW TABLE
    # ------------------------------------------------------

    if not all_reviews:

        st.info(
            "No Daily Review records available."
        )

    else:

        st.dataframe(
            all_reviews,
            use_container_width=True,
            hide_index=True
        )
