import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

from config.config import (
    ROLE_COORDINATOR,
    TASK_MASTER,
    DAILY_REVIEW
)

from utils.google_sheet import read_all

from core.navigation import logout_button

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


logout_button()


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
# DATE PARSER
# ==========================================================

def parse_date(value):

    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    text = str(
        value
    ).strip()

    if not text:
        return None

    formats = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d-%m-%y",
        "%d/%m/%y",
        "%Y-%m-%d %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                text,
                fmt
            ).date()

        except ValueError:

            continue

    try:

        parsed = pd.to_datetime(
            text,
            dayfirst=True,
            errors="coerce"
        )

        if pd.notna(parsed):

            return parsed.date()

    except Exception:

        pass

    return None


# ==========================================================
# STATUS HELPERS
# ==========================================================

def normalize_status(value):

    return str(
        value or ""
    ).strip().lower()


def is_assignment_active(assignment):

    status = normalize_status(
        assignment.get(
            "Status",
            ""
        )
    )

    return status not in {
        "removed",
        "deleted",
        "inactive"
    }


def is_task_active(task):

    return normalize_status(
        task.get(
            "Status",
            ""
        )
    ) == "active"


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

    and is_assignment_active(
        assignment
    )

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

    if normalize_status(
        assignment.get(
            "Status",
            ""
        )
    )
    == "completed"

)


pending_tasks = sum(

    1

    for assignment in my_assignments

    if normalize_status(
        assignment.get(
            "Status",
            ""
        )
    )
    == "pending"

)


in_progress_tasks = sum(

    1

    for assignment in my_assignments

    if normalize_status(
        assignment.get(
            "Status",
            ""
        )
    )
    in {
        "in progress",
        "in_progress"
    }

)


completion_percentage = (

    completed_tasks
    / total_tasks
    * 100

    if total_tasks > 0

    else 0

)


# ==========================================================
# MY REVIEW HISTORY
# ==========================================================

my_reviews = []


for review in reviews:

    review_coordinator = str(
        review.get(
            "Coordinator_ID",
            review.get(
                "Coordinator_Id",
                ""
            )
        )
    ).strip()

    if (
        review_coordinator
        == current_user_id
    ):

        my_reviews.append(
            review
        )


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
    min(
        max(
            completion_percentage / 100,
            0
        ),
        1
    )
)


st.caption(
    f"{completion_percentage:.1f}% "
    "of assigned tasks completed"
)


st.divider()


# ==========================================================
# MY ASSIGNED TASKS
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


        task_rows.append(
            {

                "Assignment ID":
                    assignment.get(
                        "Assignment_ID",
                        ""
                    ),

                "Task":
                    task_name,

                "Frequency":
                    task.get(
                        "Frequency",
                        ""
                    ),

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
                        "Pending"
                    ),

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
# DAILY REVIEW MONITORING
# ==========================================================

st.subheader(
    "📅 Daily Review Monitoring"
)


st.caption(
    "Daily tasks are expected from the assignment date "
    "through today. A missing submission is shown as "
    "Missing / Not Reporting."
)


# ==========================================================
# TODAY
# ==========================================================

today = date.today()


# ==========================================================
# ACTIVE DAILY ASSIGNMENTS
# ==========================================================

daily_assignments = []


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


    if not task:

        continue


    # Only ACTIVE tasks
    if not is_task_active(
        task
    ):

        continue


    frequency = str(
        task.get(
            "Frequency",
            ""
        )
    ).strip().lower()


    # Only Daily tasks
    if frequency != "daily":

        continue


    assigned_date = parse_date(
        assignment.get(
            "Assigned_Date",
            ""
        )
    )


    if not assigned_date:

        continue


    daily_assignments.append(
        {
            "assignment": assignment,
            "task": task,
            "task_id": task_id,
            "assigned_date": assigned_date
        }
    )


# ==========================================================
# EARLIEST DATE
# ==========================================================

if daily_assignments:

    earliest_assignment_date = min(
        item["assigned_date"]
        for item in daily_assignments
    )

else:

    earliest_assignment_date = today


# ==========================================================
# DATE FILTER
# ==========================================================

default_from_date = max(
    earliest_assignment_date,
    today - timedelta(days=30)
)


f1, f2 = st.columns(2)


with f1:

    from_date = st.date_input(
        "From Date",
        value=default_from_date,
        min_value=earliest_assignment_date,
        max_value=today,
        key="coordinator_monitor_from_final"
    )


with f2:

    to_date = st.date_input(
        "To Date",
        value=today,
        min_value=earliest_assignment_date,
        max_value=today,
        key="coordinator_monitor_to_final"
    )


# ==========================================================
# DATE VALIDATION
# ==========================================================

if from_date > to_date:

    st.warning(
        "From Date cannot be later than To Date."
    )

    st.stop()


# ==========================================================
# SUBMITTED REVIEW SET
# ==========================================================

submitted_review_keys = set()


for review in reviews:

    coordinator_id = str(
        review.get(
            "Coordinator_ID",
            review.get(
                "Coordinator_Id",
                ""
            )
        )
    ).strip()


    if coordinator_id != current_user_id:

        continue


    task_id = str(
        review.get(
            "Task_ID",
            ""
        )
    ).strip()


    review_date = parse_date(
        review.get(
            "Date",
            ""
        )
    )


    if not task_id:

        continue


    if not review_date:

        continue


    submitted_review_keys.add(
        (
            coordinator_id,
            task_id,
            review_date
        )
    )


# ==========================================================
# BUILD EXPECTED REVIEW ROWS
# ==========================================================

monitoring_rows = []


for item in daily_assignments:

    assignment = item[
        "assignment"
    ]

    task = item[
        "task"
    ]

    task_id = item[
        "task_id"
    ]

    assigned_date = item[
        "assigned_date"
    ]


    # ------------------------------------------------------
    # EXPECTED PERIOD
    # ------------------------------------------------------

    expected_start = max(
        assigned_date,
        from_date
    )


    expected_end = min(
        today,
        to_date
    )


    if expected_start > expected_end:

        continue


    current_date = expected_start


    while current_date <= expected_end:

        review_key = (
            current_user_id,
            task_id,
            current_date
        )


        submitted = (
            review_key
            in submitted_review_keys
        )


        monitoring_rows.append(
            {

                "Date":
                    current_date,

                "Task":
                    task.get(
                        "Task_Name",
                        task_id
                    ),

                "Task ID":
                    task_id,

                "Assignment ID":
                    assignment.get(
                        "Assignment_ID",
                        ""
                    ),

                "Expected":
                    "Yes",

                "Status":
                    (
                        "Submitted"
                        if submitted
                        else
                        "Missing / Not Reporting"
                    )

            }
        )


        current_date += timedelta(
            days=1
        )


# ==========================================================
# MONITORING SUMMARY
# ==========================================================

expected_count = len(
    monitoring_rows
)


submitted_count = sum(

    1

    for row in monitoring_rows

    if row[
        "Status"
    ]
    == "Submitted"

)


missing_count = sum(

    1

    for row in monitoring_rows

    if row[
        "Status"
    ]
    == "Missing / Not Reporting"

)


review_completion = (

    submitted_count
    / expected_count
    * 100

    if expected_count > 0

    else 0

)


# ==========================================================
# MONITORING METRICS
# ==========================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "📋 Expected",
        expected_count
    )


with m2:

    st.metric(
        "✅ Submitted",
        submitted_count
    )


with m3:

    st.metric(
        "⚠️ Missing",
        missing_count
    )


with m4:

    st.metric(
        "📈 Review Completion",
        f"{review_completion:.1f}%"
    )


# ==========================================================
# MONITORING PROGRESS
# ==========================================================

if expected_count > 0:

    st.progress(
        min(
            max(
                review_completion / 100,
                0
            ),
            1
        )
    )


# ==========================================================
# MONITORING DETAIL
# ==========================================================

if monitoring_rows:

    monitoring_df = pd.DataFrame(
        monitoring_rows
    )


    monitoring_df = (
        monitoring_df
        .sort_values(
            by=[
                "Date",
                "Task"
            ],
            ascending=[
                False,
                True
            ]
        )
    )


    monitoring_df[
        "Date"
    ] = pd.to_datetime(
        monitoring_df[
            "Date"
        ]
    ).dt.strftime(
        "%d-%m-%Y"
    )


    st.dataframe(
        monitoring_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No active Daily tasks have expected "
        "review dates in the selected period."
    )


st.divider()


# ==========================================================
# MY REVIEW HISTORY
# ==========================================================

st.subheader(
    "📚 My Review History"
)


if my_reviews:

    history_rows = []


    for review in my_reviews:

        history_rows.append(
            {

                "Review ID":
                    review.get(
                        "Review_ID",
                        ""
                    ),

                "Date":
                    review.get(
                        "Date",
                        ""
                    ),

                "Task ID":
                    review.get(
                        "Task_ID",
                        ""
                    ),

                "Assignment ID":
                    review.get(
                        "Assignment_ID",
                        ""
                    ),

                "Status":
                    review.get(
                        "Status",
                        ""
                    ),

                "Remarks":
                    review.get(
                        "Remarks",
                        ""
                    ),

                "Submitted At":
                    review.get(
                        "Submitted_At",
                        ""
                    )

            }
        )


    history_df = pd.DataFrame(
        history_rows
    )


    if not history_df.empty:

        history_df[
            "_SortDate"
        ] = history_df[
            "Date"
        ].apply(
            parse_date
        )


        history_df = (
            history_df
            .sort_values(
                by="_SortDate",
                ascending=False
            )
            .drop(
                columns=[
                    "_SortDate"
                ]
            )
        )


    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No Daily Reviews submitted yet."
    )


st.divider()


# ==========================================================
# QUICK ACTIONS
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
