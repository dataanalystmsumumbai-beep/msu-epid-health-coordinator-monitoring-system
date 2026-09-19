import streamlit as st
import pandas as pd

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from config.config import (
    ROLE_COORDINATOR,
    TASK_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW,
)

from utils.google_sheet import read_all
from core.navigation import logout_button
from services.task_assignment_service import TaskAssignmentService


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Coordinator Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# LOGIN CHECK
# ============================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access the Coordinator Dashboard.")
    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

current_user_id = str(
    st.session_state.get(
        "user_id",
        st.session_state.get("username", "")
    )
).strip()

current_username = str(
    st.session_state.get(
        "username",
        current_user_id
    )
).strip()

current_role = str(
    st.session_state.get("role", "")
).strip()


# ============================================================
# ACCESS CONTROL
# ============================================================

if current_role != ROLE_COORDINATOR:
    st.error("Access denied. This page is only available to Coordinators.")
    st.stop()


# ============================================================
# SIDEBAR / LOGOUT
# ============================================================

logout_button()


# ============================================================
# INDIA TIMEZONE
# ============================================================

INDIA_TZ = ZoneInfo("Asia/Kolkata")

now_india = datetime.now(INDIA_TZ)
today = now_india.date()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📊 Coordinator Dashboard")

st.caption(
    f"Welcome, {current_username} | "
    f"Today: {today.strftime('%d-%m-%Y')}"
)


# ============================================================
# SAFE READ
# ============================================================

def safe_read(sheet_name):
    try:
        data = read_all(sheet_name)

        if data is None:
            return []

        return data

    except Exception:
        return []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_status(value):
    return str(value).strip().upper()


def parse_date(value):
    """
    Converts common date formats into Python date.
    """

    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    text = str(value).strip()

    if not text:
        return None

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%d-%b-%Y",
        "%d %b %Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            pass

    try:
        return pd.to_datetime(text, dayfirst=True).date()
    except Exception:
        return None


def is_assignment_active(row):
    """
    Assignment is considered active unless it is explicitly
    removed/deleted/inactive.
    """

    status = normalize_status(row.get("Status", ""))

    if status in {
        "REMOVED",
        "DELETED",
        "INACTIVE",
        "CANCELLED",
    }:
        return False

    return True


def is_task_active(task):
    """
    Only explicit ACTIVE tasks are allowed for Daily Review
    monitoring.
    """

    return normalize_status(task.get("Status", "")) == "ACTIVE"


# ============================================================
# LOAD MASTER DATA
# ============================================================

all_tasks = safe_read(TASK_MASTER)
all_assignments = safe_read(COORDINATOR_TASK_MAP)
all_reviews = safe_read(DAILY_REVIEW)


# ============================================================
# CONVERT TO DATAFRAMES
# ============================================================

tasks_df = pd.DataFrame(all_tasks)
assignments_df = pd.DataFrame(all_assignments)
reviews_df = pd.DataFrame(all_reviews)


# ============================================================
# MY ASSIGNMENTS
# ============================================================

my_assignments = [
    row
    for row in all_assignments
    if str(
        row.get("Coordinator_ID", "")
    ).strip() == current_user_id
    and is_assignment_active(row)
]


# ============================================================
# TASK LOOKUP
# ============================================================

task_lookup = {}

for task in all_tasks:

    task_id = str(
        task.get("Task_ID", "")
    ).strip()

    if task_id:
        task_lookup[task_id] = task


# ============================================================
# TOP METRICS
# ============================================================

assigned_count = len(my_assignments)

completed_count = 0
pending_count = 0
in_progress_count = 0

for assignment in my_assignments:

    status = normalize_status(
        assignment.get("Status", "")
    )

    if status == "COMPLETED":
        completed_count += 1

    elif status == "IN PROGRESS":
        in_progress_count += 1

    elif status in {
        "PENDING",
        "ASSIGNED",
        "NOT STARTED",
        "",
    }:
        pending_count += 1


if assigned_count > 0:
    assignment_completion = (
        completed_count / assigned_count
    ) * 100
else:
    assignment_completion = 0


# ============================================================
# TOP METRIC CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "📌 Assigned",
        assigned_count
    )

with col2:
    st.metric(
        "✅ Completed",
        completed_count
    )

with col3:
    st.metric(
        "⏳ Pending",
        pending_count
    )

with col4:
    st.metric(
        "🔄 In Progress",
        in_progress_count
    )

with col5:
    st.metric(
        "📈 Completion",
        f"{assignment_completion:.1f}%"
    )


st.divider()


# ============================================================
# MY ASSIGNED TASKS
# ============================================================

st.subheader("📋 My Assigned Tasks")


assigned_display = []

for assignment in my_assignments:

    task_id = str(
        assignment.get("Task_ID", "")
    ).strip()

    task = task_lookup.get(task_id, {})

    assigned_display.append(
        {
            "Assignment ID": assignment.get(
                "Assignment_ID",
                ""
            ),
            "Task ID": task_id,
            "Task Name": task.get(
                "Task_Name",
                "Not Found"
            ),
            "Category": task.get(
                "Category",
                ""
            ),
            "Frequency": task.get(
                "Frequency",
                ""
            ),
            "Priority": assignment.get(
                "Priority",
                task.get("Priority", "")
            ),
            "Assigned Date": assignment.get(
                "Assigned_Date",
                ""
            ),
            "Due Date": assignment.get(
                "Due_Date",
                ""
            ),
            "Status": assignment.get(
                "Status",
                ""
            ),
            "Remarks": assignment.get(
                "Remarks",
                ""
            ),
        }
    )


if assigned_display:

    assigned_df = pd.DataFrame(
        assigned_display
    )

    st.dataframe(
        assigned_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No active task assignments found."
    )


st.divider()


# ============================================================
# MY REVIEW HISTORY
# ============================================================

st.subheader("📝 My Review History")


my_reviews = []

for review in all_reviews:

    coordinator_id = str(
        review.get("Coordinator_ID", "")
    ).strip()

    username = str(
        review.get("Username", "")
    ).strip()

    coordinator_id_alt = str(
        review.get("Coordinator_Id", "")
    ).strip()

    if (
        coordinator_id == current_user_id
        or coordinator_id_alt == current_user_id
        or username == current_username
    ):
        my_reviews.append(review)


if my_reviews:

    history_display = []

    for review in my_reviews:

        task_id = str(
            review.get("Task_ID", "")
        ).strip()

        task = task_lookup.get(
            task_id,
            {}
        )

        history_display.append(
            {
                "Review ID": review.get(
                    "Review_ID",
                    ""
                ),
                "Date": review.get(
                    "Date",
                    ""
                ),
                "Task": task.get(
                    "Task_Name",
                    task_id
                ),
                "Task ID": task_id,
                "Assignment ID": review.get(
                    "Assignment_ID",
                    ""
                ),
                "Status": review.get(
                    "Status",
                    ""
                ),
                "Remarks": review.get(
                    "Remarks",
                    ""
                ),
                "Submitted At": review.get(
                    "Submitted_At",
                    ""
                ),
            }
        )

    history_df = pd.DataFrame(
        history_display
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No Daily Review history found."
    )


st.divider()


# ============================================================
# DAILY REVIEW MONITORING
# ============================================================

st.subheader("📅 Daily Review Monitoring")

st.caption(
    "Daily tasks are expected from the assignment date "
    "through today. A missing submission is shown as "
    "Missing / Not Reporting."
)


# ============================================================
# ACTIVE DAILY ASSIGNMENTS
# ============================================================

active_daily_assignments = []

for assignment in my_assignments:

    task_id = str(
        assignment.get("Task_ID", "")
    ).strip()

    task = task_lookup.get(
        task_id,
        {}
    )

    if not task:
        continue

    if not is_task_active(task):
        continue

    frequency = normalize_status(
        task.get("Frequency", "")
    )

    if frequency != "DAILY":
        continue

    active_daily_assignments.append(
        {
            "assignment": assignment,
            "task": task,
        }
    )


# ============================================================
# DATE RANGE
# ============================================================

if active_daily_assignments:

    assignment_dates = []

    for item in active_daily_assignments:

        assignment = item["assignment"]

        assigned_date = parse_date(
            assignment.get(
                "Assigned_Date",
                ""
            )
        )

        if assigned_date:
            assignment_dates.append(
                assigned_date
            )

    if assignment_dates:

        earliest_assignment_date = min(
            assignment_dates
        )

    else:

        earliest_assignment_date = today

else:

    earliest_assignment_date = today


default_from_date = max(
    earliest_assignment_date,
    today - timedelta(days=30)
)


date_col1, date_col2 = st.columns(2)

with date_col1:

    from_date = st.date_input(
        "From Date",
        value=default_from_date,
        min_value=earliest_assignment_date,
        max_value=today,
        key="coordinator_monitor_from_date",
    )


with date_col2:

    to_date = st.date_input(
        "To Date",
        value=today,
        min_value=earliest_assignment_date,
        max_value=today,
        key="coordinator_monitor_to_date",
    )


if from_date > to_date:

    st.error(
        "From Date cannot be greater than To Date."
    )

    st.stop()


# ============================================================
# SUBMITTED REVIEW KEYS
# ============================================================

submitted_review_keys = set()

for review in all_reviews:

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

    if not task_id or not review_date:

        continue

    submitted_review_keys.add(
        (
            coordinator_id,
            task_id,
            review_date,
        )
    )


# ============================================================
# BUILD MONITORING DATA
# ============================================================

monitoring_rows = []

# Prevent duplicate expected rows when the same
# Coordinator + Task + Date appears through multiple
# assignment records.
expected_keys = set()


for item in active_daily_assignments:

    assignment = item["assignment"]
    task = item["task"]

    task_id = str(
        task.get(
            "Task_ID",
            ""
        )
    ).strip()

    task_name = str(
        task.get(
            "Task_Name",
            task_id
        )
    ).strip()

    assignment_id = str(
        assignment.get(
            "Assignment_ID",
            ""
        )
    ).strip()

    assigned_date = parse_date(
        assignment.get(
            "Assigned_Date",
            ""
        )
    )

    due_date = parse_date(
        assignment.get(
            "Due_Date",
            ""
        )
    )

    if assigned_date is None:

        assigned_date = from_date

    start_date = max(
        assigned_date,
        from_date
    )

    end_date = min(
        today,
        to_date
    )

    # If a due date exists, do not expect reviews
    # beyond that assignment's due date.
    if due_date:

        end_date = min(
            end_date,
            due_date
        )

    if start_date > end_date:

        continue

    current_date = start_date

    while current_date <= end_date:

        expected_key = (
            current_user_id,
            task_id,
            current_date,
        )

        # Avoid double-counting duplicate assignments.
        if expected_key not in expected_keys:

            expected_keys.add(
                expected_key
            )

            submitted = (
                expected_key
                in submitted_review_keys
            )

            if submitted:

                status = "Submitted"

            else:

                status = "Missing / Not Reporting"

            monitoring_rows.append(
                {
                    "Date": current_date,
                    "Task ID": task_id,
                    "Task Name": task_name,
                    "Assignment ID": assignment_id,
                    "Status": status,
                }
            )

        current_date += timedelta(days=1)


# ============================================================
# MONITORING SUMMARY
# ============================================================

expected_count = len(
    monitoring_rows
)

submitted_count = sum(
    1
    for row in monitoring_rows
    if row["Status"] == "Submitted"
)

missing_count = sum(
    1
    for row in monitoring_rows
    if row["Status"] == "Missing / Not Reporting"
)


if expected_count > 0:

    review_completion = (
        submitted_count / expected_count
    ) * 100

else:

    review_completion = 0


# ============================================================
# MONITORING METRIC CARDS
# ============================================================

mon1, mon2, mon3, mon4 = st.columns(4)

with mon1:

    st.metric(
        "Expected",
        expected_count
    )

with mon2:

    st.metric(
        "Submitted",
        submitted_count
    )

with mon3:

    st.metric(
        "Missing",
        missing_count
    )

with mon4:

    st.metric(
        "Review Completion",
        f"{review_completion:.1f}%"
    )


# ============================================================
# PROGRESS BAR
# ============================================================

st.progress(
    min(
        max(
            review_completion / 100,
            0.0
        ),
        1.0
    )
)


# ============================================================
# DATE-WISE BREAKDOWN
# ============================================================

st.markdown("### 📆 Date-wise Review Breakdown")


if monitoring_rows:

    date_summary_rows = []

    date_groups = {}

    for row in monitoring_rows:

        review_date = row["Date"]

        if review_date not in date_groups:

            date_groups[review_date] = {
                "Expected": 0,
                "Submitted": 0,
                "Missing": 0,
            }

        date_groups[review_date]["Expected"] += 1

        if row["Status"] == "Submitted":

            date_groups[review_date]["Submitted"] += 1

        else:

            date_groups[review_date]["Missing"] += 1


    for review_date in sorted(
        date_groups.keys()
    ):

        values = date_groups[
            review_date
        ]

        expected = values["Expected"]
        submitted = values["Submitted"]
        missing = values["Missing"]

        if expected > 0:

            completion = (
                submitted / expected
            ) * 100

        else:

            completion = 0

        date_summary_rows.append(
            {
                "Date": review_date.strftime(
                    "%d-%m-%Y"
                ),
                "Expected": expected,
                "Submitted": submitted,
                "Missing": missing,
                "Completion %": round(
                    completion,
                    1
                ),
            }
        )


    date_summary_df = pd.DataFrame(
        date_summary_rows
    )

    st.dataframe(
        date_summary_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No Daily Review monitoring data "
        "is available for the selected date range."
    )


# ============================================================
# TASK-WISE BREAKDOWN
# ============================================================

st.markdown("### 📋 Task-wise Review Breakdown")


if monitoring_rows:

    task_summary_rows = []

    task_groups = {}

    for row in monitoring_rows:

        task_key = (
            row["Task ID"],
            row["Task Name"],
        )

        if task_key not in task_groups:

            task_groups[task_key] = {
                "Expected": 0,
                "Submitted": 0,
                "Missing": 0,
            }

        task_groups[task_key]["Expected"] += 1

        if row["Status"] == "Submitted":

            task_groups[task_key]["Submitted"] += 1

        else:

            task_groups[task_key]["Missing"] += 1


    for (
        task_id,
        task_name,
    ) in sorted(
        task_groups.keys(),
        key=lambda x: (
            str(x[1]).lower(),
            str(x[0]).lower(),
        ),
    ):

        values = task_groups[
            (
                task_id,
                task_name,
            )
        ]

        expected = values["Expected"]
        submitted = values["Submitted"]
        missing = values["Missing"]

        if expected > 0:

            completion = (
                submitted / expected
            ) * 100

        else:

            completion = 0

        task_summary_rows.append(
            {
                "Task ID": task_id,
                "Task Name": task_name,
                "Expected": expected,
                "Submitted": submitted,
                "Missing": missing,
                "Completion %": round(
                    completion,
                    1
                ),
            }
        )


    task_summary_df = pd.DataFrame(
        task_summary_rows
    )

    st.dataframe(
        task_summary_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No task-wise monitoring data "
        "is available."
    )


# ============================================================
# DETAILED MONITORING
# ============================================================

st.markdown("### 🔎 Detailed Daily Review Status")


if monitoring_rows:

    detail_rows = []

    for row in sorted(
        monitoring_rows,
        key=lambda x: (
            x["Date"],
            x["Task Name"],
        ),
        reverse=True,
    ):

        detail_rows.append(
            {
                "Date": row["Date"].strftime(
                    "%d-%m-%Y"
                ),
                "Task ID": row["Task ID"],
                "Task Name": row["Task Name"],
                "Assignment ID": row["Assignment ID"],
                "Status": row["Status"],
            }
        )


    detail_df = pd.DataFrame(
        detail_rows
    )

    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No detailed review records available."
    )


st.divider()


# ============================================================
# QUICK ACTIONS
# ============================================================

st.subheader("⚡ Quick Actions")

quick_col1, quick_col2 = st.columns(2)

with quick_col1:

    if st.button(
        "📋 Task Management",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/04_Task_Management.py"
        )


with quick_col2:

    if st.button(
        "📝 Daily Review",
        use_container_width=True,
    ):

        st.switch_page(
            "pages/03_Daily_Review.py"
        )
