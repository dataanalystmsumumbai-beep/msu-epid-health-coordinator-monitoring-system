import streamlit as st
import pandas as pd
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
    COORDINATOR_TASK_MAP,
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Daily Review",
    page_icon="📝",
    layout="wide"
)


# ==========================================================
# ACCESS
# ==========================================================

require_login([
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
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

    if not record:
        return ""

    for key in keys:

        value = record.get(
            key,
            ""
        )

        if (
            value is not None
            and str(value).strip() != ""
        ):
            return value

    return ""


def normalize(value):

    return str(
        value if value is not None else ""
    ).strip()


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    all_tasks = (
        TaskService
        .get_all_tasks()
    )

except Exception:

    all_tasks = []


try:

    all_assignments = (
        TaskAssignmentService
        .get_all_assignments()
    )

except Exception:

    all_assignments = []


try:

    all_reviews = read_all(
        DAILY_REVIEW
    )

except Exception:

    all_reviews = []


all_tasks = all_tasks or []
all_assignments = all_assignments or []
all_reviews = all_reviews or []


# ==========================================================
# TASK LOOKUP
# ==========================================================

task_lookup = {}

for task in all_tasks:

    task_id = normalize(
        get_value(
            task,
            "Task_ID",
            "Task_Id",
            "ID"
        )
    )

    if task_id:

        task_lookup[
            task_id
        ] = task


# ==========================================================
# ASSIGNMENT FILTER
# ==========================================================

if current_role == ROLE_COORDINATOR:

    assigned_records = [

        assignment

        for assignment in all_assignments

        if normalize(
            get_value(
                assignment,
                "Coordinator_ID",
                "Coordinator_Id"
            )
        )
        == current_user_id

        and normalize(
            get_value(
                assignment,
                "Status"
            )
        ).lower()

        not in [
            "removed",
            "inactive",
            "deleted"
        ]

    ]

else:

    assigned_records = list(
        all_assignments
    )


# ==========================================================
# BUILD ASSIGNED TASK LIST
# ==========================================================

assigned_tasks = []

for assignment in assigned_records:

    task_id = normalize(
        get_value(
            assignment,
            "Task_ID",
            "Task_Id"
        )
    )

    task = task_lookup.get(
        task_id,
        {}
    )

    task_name = normalize(
        get_value(
            task,
            "Task_Name",
            "Task",
            "Name"
        )
    )

    if not task_name:

        task_name = normalize(
            get_value(
                assignment,
                "Task_Name",
                "Task"
            )
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

if current_role == ROLE_COORDINATOR:

    st.subheader(
        "📋 My Assigned Tasks"
    )

    total_tasks = len(
        assigned_tasks
    )

    completed_tasks = 0
    in_progress_tasks = 0
    pending_tasks = 0

    for item in assigned_tasks:

        status = normalize(
            get_value(
                item["assignment"],
                "Status"
            )
        ).lower()

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
            "🔄 In Progress",
            in_progress_tasks
        )

    with c4:

        st.metric(
            "📈 Completion",
            f"{completion_rate:.0f}%"
        )


    if total_tasks > 0:

        st.progress(
            completion_rate / 100
        )

    st.caption(
        f"Overall task completion: "
        f"{completion_rate:.1f}%"
    )

    st.divider()


    # ======================================================
    # SUBMIT DAILY REVIEW
    # ======================================================

    st.subheader(
        "📝 Submit Daily Review"
    )

    if not assigned_tasks:

        st.info(
            "No active tasks are currently assigned to you."
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

            due_date = normalize(
                get_value(
                    assignment,
                    "Due_Date",
                    "Due Date"
                )
            )

            label = task_name or task_id

            if due_date:

                label = (
                    f"{label} | "
                    f"Due: {due_date}"
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


        selected_item = None

        for item in assigned_tasks:

            if (
                item["task_id"]
                == selected_task_id
            ):

                selected_item = item

                break


        selected_assignment = (
            selected_item["assignment"]
            if selected_item
            else {}
        )


        assignment_id = normalize(
            get_value(
                selected_assignment,
                "Assignment_ID",
                "Assignment_Id",
                "ID"
            )
        )


        st.info(
            f"Selected Task: "
            f"**{task_options.get(selected_task_id, selected_task_id)}**"
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
                "Enter today's work, progress, "
                "observations or pending reason."
            ),
            height=150,
            key="review_remarks"
        )


        submit_review = st.button(
            "✅ Submit Daily Review",
            type="primary",
            use_container_width=True,
            key="submit_daily_review"
        )


        if submit_review:

            review_date_text = (
                review_date.strftime(
                    "%d-%m-%Y"
                )
            )


            # ----------------------------------------------
            # VALIDATION
            # ----------------------------------------------

            if not selected_task_id:

                st.error(
                    "Please select a task."
                )

                st.stop()


            if (
                review_status != "Pending"
                and not remarks.strip()
            ):

                st.error(
                    "Please enter the progress / remarks."
                )

                st.stop()


            # ----------------------------------------------
            # DUPLICATE CHECK
            # ----------------------------------------------

            duplicate = False

            for review in all_reviews:

                existing_coordinator = normalize(
                    get_value(
                        review,
                        "Coordinator_ID",
                        "Coordinator_Id",
                        "User_ID",
                        "Username"
                    )
                )

                existing_task = normalize(
                    get_value(
                        review,
                        "Task_ID",
                        "Task_Id"
                    )
                )

                existing_date = normalize(
                    get_value(
                        review,
                        "Review_Date",
                        "Date"
                    )
                )


                if (

                    existing_coordinator
                    == current_user_id

                    and

                    existing_task
                    == selected_task_id

                    and

                    existing_date
                    == review_date_text

                    and

                    normalize(
                        get_value(
                            review,
                            "Status"
                        )
                    ).upper()
                    != "DELETED"

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

                    review_id = (
                        "REV-"
                        + datetime.now().strftime(
                            "%Y%m%d%H%M%S%f"
                        )[:20]
                    )


                    submitted_on = (
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    )


                    # ------------------------------------------
                    # DAILY REVIEW SHEET
                    #
                    # 1 Review_ID
                    # 2 Date
                    # 3 Coordinator_ID
                    # 4 Task_ID
                    # 5 Assignment_ID
                    # 6 Status
                    # 7 Remarks
                    # 8 Submitted_At
                    # ------------------------------------------

                    row = [

                        review_id,

                        review_date_text,

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


                    # ------------------------------------------
                    # UPDATE ASSIGNMENT STATUS
                    # ------------------------------------------

                    assignment_row = None

                    for row_number, assignment in enumerate(
                        all_assignments,
                        start=2
                    ):

                        existing_assignment_id = normalize(
                            get_value(
                                assignment,
                                "Assignment_ID",
                                "Assignment_Id",
                                "ID"
                            )
                        )

                        if (
                            existing_assignment_id
                            == assignment_id
                        ):

                            assignment_row = (
                                row_number
                            )

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


    # ======================================================
    # COORDINATOR REVIEW HISTORY
    # ======================================================

    st.subheader(
        "📚 My Review History"
    )


    my_reviews = [

        review

        for review in all_reviews

        if normalize(
            get_value(
                review,
                "Coordinator_ID",
                "Coordinator_Id",
                "User_ID",
                "Username"
            )
        )
        == current_user_id

        and

        normalize(
            get_value(
                review,
                "Status"
            )
        ).upper()
        != "DELETED"

    ]


    if not my_reviews:

        st.info(
            "No Daily Reviews submitted yet."
        )

    else:

        history_rows = []

        for review in my_reviews:

            task_id = normalize(
                get_value(
                    review,
                    "Task_ID",
                    "Task_Id"
                )
            )

            task = task_lookup.get(
                task_id,
                {}
            )

            task_name = normalize(
                get_value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )
            )

            if not task_name:

                task_name = task_id


            history_rows.append(
                {
                    "Review ID":
                        get_value(
                            review,
                            "Review_ID"
                        ),

                    "Date":
                        get_value(
                            review,
                            "Date",
                            "Review_Date"
                        ),

                    "Task":
                        task_name,

                    "Status":
                        get_value(
                            review,
                            "Status"
                        ),

                    "Remarks":
                        get_value(
                            review,
                            "Remarks"
                        ),

                    "Submitted At":
                        get_value(
                            review,
                            "Submitted_At"
                        )
                }
            )


        st.dataframe(
            pd.DataFrame(
                history_rows
            ),
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# ADMIN / DEVELOPER MONITORING
# ==========================================================

else:

    st.subheader(
        "📊 Daily Review Monitoring"
    )


    # ======================================================
    # METRICS
    # ======================================================

    active_reviews = [

        review

        for review in all_reviews

        if normalize(
            get_value(
                review,
                "Status"
            )
        ).upper()
        != "DELETED"

    ]


    total_reviews = len(
        active_reviews
    )


    completed_reviews = sum(

        1

        for review in active_reviews

        if normalize(
            get_value(
                review,
                "Status"
            )
        ).lower()
        == "completed"

    )


    pending_reviews = sum(

        1

        for review in active_reviews

        if normalize(
            get_value(
                review,
                "Status"
            )
        ).lower()
        == "pending"

    )


    in_progress_reviews = sum(

        1

        for review in active_reviews

        if normalize(
            get_value(
                review,
                "Status"
            )
        ).lower()
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


    # ======================================================
    # COORDINATOR-WISE SUMMARY
    # ======================================================

    st.subheader(
        "👨‍⚕️ Coordinator-wise Review Summary"
    )


    coordinator_summary = {}


    for review in active_reviews:

        coordinator_id = normalize(
            get_value(
                review,
                "Coordinator_ID",
                "Coordinator_Id",
                "User_ID",
                "Username"
            )
        )

        if not coordinator_id:

            coordinator_id = "Unknown"


        if coordinator_id not in coordinator_summary:

            coordinator_summary[
                coordinator_id
            ] = {
                "Total": 0,
                "Completed": 0,
                "In Progress": 0,
                "Pending": 0
            }


        coordinator_summary[
            coordinator_id
        ]["Total"] += 1


        status = normalize(
            get_value(
                review,
                "Status"
            )
        ).lower()


        if status == "completed":

            coordinator_summary[
                coordinator_id
            ]["Completed"] += 1

        elif status in [
            "in progress",
            "in_progress"
        ]:

            coordinator_summary[
                coordinator_id
            ]["In Progress"] += 1

        elif status == "pending":

            coordinator_summary[
                coordinator_id
            ]["Pending"] += 1


    summary_rows = []


    for coordinator_id, values in (
        coordinator_summary.items()
    ):

        total = values[
            "Total"
        ]

        completed = values[
            "Completed"
        ]

        completion = (

            completed
            / total
            * 100

            if total
            else 0

        )


        summary_rows.append(
            {
                "Coordinator":
                    coordinator_id,

                "Total Reviews":
                    total,

                "Completed":
                    completed,

                "In Progress":
                    values[
                        "In Progress"
                    ],

                "Pending":
                    values[
                        "Pending"
                    ],

                "Completion %":
                    round(
                        completion,
                        1
                    )
            }
        )


    if summary_rows:

        st.dataframe(
            pd.DataFrame(
                summary_rows
            ),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No Coordinator review data available."
        )


    st.divider()


    # ======================================================
    # ALL REVIEWS
    # ======================================================

    st.subheader(
        "📋 All Daily Reviews"
    )


    if not active_reviews:

        st.info(
            "No Daily Review records available."
        )

    else:

        display_rows = []


        for review in active_reviews:

            task_id = normalize(
                get_value(
                    review,
                    "Task_ID",
                    "Task_Id"
                )
            )


            task = task_lookup.get(
                task_id,
                {}
            )


            task_name = normalize(
                get_value(
                    task,
                    "Task_Name",
                    "Task",
                    "Name"
                )
            )


            if not task_name:

                task_name = task_id


            display_rows.append(
                {
                    "Review ID":
                        get_value(
                            review,
                            "Review_ID"
                        ),

                    "Date":
                        get_value(
                            review,
                            "Date",
                            "Review_Date"
                        ),

                    "Coordinator":
                        get_value(
                            review,
                            "Coordinator_ID",
                            "Coordinator_Id",
                            "User_ID",
                            "Username"
                        ),

                    "Task":
                        task_name,

                    "Status":
                        get_value(
                            review,
                            "Status"
                        ),

                    "Remarks":
                        get_value(
                            review,
                            "Remarks"
                        ),

                    "Submitted At":
                        get_value(
                            review,
                            "Submitted_At"
                        )
                }
            )


        st.dataframe(
            pd.DataFrame(
                display_rows
            ),
            use_container_width=True,
            hide_index=True
        )
