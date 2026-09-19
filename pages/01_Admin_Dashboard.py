import streamlit as st
import pandas as pd

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from config.config import (
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    TASK_MASTER,
    COORDINATOR_MASTER,
    COORDINATOR_TASK_MAP,
    DAILY_REVIEW,
)

from utils.google_sheet import read_all
from core.navigation import logout_button


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Admin Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# LOGIN CHECK
# ============================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access this dashboard.")
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

allowed_roles = {
    ROLE_ADMIN,
    ROLE_DEVELOPER,
    "Admin",
    "Developer",
    "ADMIN",
    "DEVELOPER",
}

if current_role not in allowed_roles:
    st.error(
        "Access denied. This dashboard is available only "
        "to Admin and Developer users."
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

logout_button()


# ============================================================
# INDIA TIMEZONE
# ============================================================

INDIA_TZ = ZoneInfo("Asia/Kolkata")

now_india = datetime.now(INDIA_TZ)
today = now_india.date()


# ============================================================
# HEADER
# ============================================================

st.title("📊 Admin Monitoring Dashboard")

st.caption(
    f"Welcome, {current_username} | "
    f"Role: {current_role} | "
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
# HELPERS
# ============================================================

def normalize_status(value):

    return str(value).strip().upper()


def parse_date(value):

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
            return datetime.strptime(
                text,
                fmt
            ).date()

        except Exception:
            pass

    try:

        return pd.to_datetime(
            text,
            dayfirst=True
        ).date()

    except Exception:

        return None


def is_assignment_active(row):

    status = normalize_status(
        row.get("Status", "")
    )

    return status not in {
        "REMOVED",
        "DELETED",
        "INACTIVE",
        "CANCELLED",
    }


def is_task_active(row):

    return normalize_status(
        row.get("Status", "")
    ) == "ACTIVE"


# ============================================================
# LOAD DATA
# ============================================================

all_tasks = safe_read(TASK_MASTER)

all_coordinators = safe_read(
    COORDINATOR_MASTER
)

all_assignments = safe_read(
    COORDINATOR_TASK_MAP
)

all_reviews = safe_read(
    DAILY_REVIEW
)


# ============================================================
# DATAFRAMES
# ============================================================

tasks_df = pd.DataFrame(all_tasks)

coordinators_df = pd.DataFrame(
    all_coordinators
)

assignments_df = pd.DataFrame(
    all_assignments
)

reviews_df = pd.DataFrame(
    all_reviews
)


# ============================================================
# TASK LOOKUP
# ============================================================

task_lookup = {}

for task in all_tasks:

    task_id = str(
        task.get(
            "Task_ID",
            ""
        )
    ).strip()

    if task_id:

        task_lookup[task_id] = task


# ============================================================
# COORDINATOR LOOKUP
# ============================================================

coordinator_lookup = {}

for coordinator in all_coordinators:

    coordinator_id = str(
        coordinator.get(
            "Coordinator_ID",
            ""
        )
    ).strip()

    if coordinator_id:

        coordinator_lookup[
            coordinator_id
        ] = coordinator


# ============================================================
# ACTIVE DAILY TASKS
# ============================================================

active_daily_tasks = {}

for task in all_tasks:

    task_id = str(
        task.get(
            "Task_ID",
            ""
        )
    ).strip()

    frequency = normalize_status(
        task.get(
            "Frequency",
            ""
        )
    )

    if (
        task_id
        and is_task_active(task)
        and frequency == "DAILY"
    ):

        active_daily_tasks[
            task_id
        ] = task


# ============================================================
# ACTIVE DAILY ASSIGNMENTS
# ============================================================

active_daily_assignments = []

for assignment in all_assignments:

    if not is_assignment_active(
        assignment
    ):
        continue

    task_id = str(
        assignment.get(
            "Task_ID",
            ""
        )
    ).strip()

    coordinator_id = str(
        assignment.get(
            "Coordinator_ID",
            ""
        )
    ).strip()

    if not coordinator_id:
        continue

    if task_id not in active_daily_tasks:
        continue

    active_daily_assignments.append(
        {
            "assignment": assignment,
            "task": active_daily_tasks[
                task_id
            ],
        }
    )


# ============================================================
# DATE RANGE
# ============================================================

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


default_from_date = max(
    earliest_assignment_date,
    today - timedelta(days=30)
)


st.markdown("### 📅 Monitoring Period")


date_col1, date_col2 = st.columns(2)

with date_col1:

    from_date = st.date_input(
        "From Date",
        value=default_from_date,
        min_value=earliest_assignment_date,
        max_value=today,
        key="admin_monitor_from_date",
    )


with date_col2:

    to_date = st.date_input(
        "To Date",
        value=today,
        min_value=earliest_assignment_date,
        max_value=today,
        key="admin_monitor_to_date",
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

    if (
        coordinator_id
        and task_id
        and review_date
    ):

        submitted_review_keys.add(
            (
                coordinator_id,
                task_id,
                review_date,
            )
        )


# ============================================================
# BUILD EXPECTED MONITORING ROWS
# ============================================================

monitoring_rows = []

# Important:
# Coordinator + Task + Date is treated as one expected
# Daily Review, even if duplicate assignment rows exist.

expected_keys = set()


for item in active_daily_assignments:

    assignment = item["assignment"]

    task = item["task"]

    coordinator_id = str(
        assignment.get(
            "Coordinator_ID",
            ""
        )
    ).strip()

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
            coordinator_id,
            task_id,
            current_date,
        )

        if expected_key not in expected_keys:

            expected_keys.add(
                expected_key
            )

            submitted = (
                expected_key
                in submitted_review_keys
            )

            monitoring_rows.append(
                {
                    "Date": current_date,
                    "Coordinator_ID": coordinator_id,
                    "Task_ID": task_id,
                    "Task_Name": task_name,
                    "Assignment_ID": assignment_id,
                    "Status": (
                        "Submitted"
                        if submitted
                        else "Missing / Not Reporting"
                    ),
                }
            )

        current_date += timedelta(days=1)


# ============================================================
# OVERALL SUMMARY
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


if expected_count:

    completion_percentage = (
        submitted_count
        / expected_count
    ) * 100

else:

    completion_percentage = 0


# ============================================================
# SUMMARY CARDS
# ============================================================

st.markdown("### 📌 Overall Daily Review Summary")


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Expected",
        expected_count
    )

with col2:

    st.metric(
        "Submitted",
        submitted_count
    )

with col3:

    st.metric(
        "Missing",
        missing_count
    )

with col4:

    st.metric(
        "Completion",
        f"{completion_percentage:.1f}%"
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


st.divider()


# ============================================================
# COORDINATOR-WISE MONITORING
# ============================================================

st.subheader("👥 Coordinator-wise Monitoring")


if monitoring_rows:

    coordinator_groups = {}

    for row in monitoring_rows:

        coordinator_id = row[
            "Coordinator_ID"
        ]

        if coordinator_id not in coordinator_groups:

            coordinator_groups[
                coordinator_id
            ] = {
                "Expected": 0,
                "Submitted": 0,
                "Missing": 0,
            }

        coordinator_groups[
            coordinator_id
        ]["Expected"] += 1

        if row["Status"] == "Submitted":

            coordinator_groups[
                coordinator_id
            ]["Submitted"] += 1

        else:

            coordinator_groups[
                coordinator_id
            ]["Missing"] += 1


    coordinator_rows = []

    for coordinator_id in sorted(
        coordinator_groups.keys()
    ):

        values = coordinator_groups[
            coordinator_id
        ]

        expected = values[
            "Expected"
        ]

        submitted = values[
            "Submitted"
        ]

        missing = values[
            "Missing"
        ]

        if expected:

            completion = (
                submitted
                / expected
            ) * 100

        else:

            completion = 0

        coordinator = coordinator_lookup.get(
            coordinator_id,
            {}
        )

        coordinator_name = (
            coordinator.get(
                "Coordinator_Name",
                coordinator.get(
                    "Name",
                    coordinator.get(
                        "Username",
                        coordinator_id
                    )
                )
            )
        )

        coordinator_rows.append(
            {
                "Coordinator ID": coordinator_id,
                "Coordinator Name": coordinator_name,
                "Expected": expected,
                "Submitted": submitted,
                "Missing": missing,
                "Completion %": round(
                    completion,
                    1
                ),
            }
        )


    coordinator_summary_df = pd.DataFrame(
        coordinator_rows
    )

    st.dataframe(
        coordinator_summary_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No coordinator monitoring data "
        "is available for the selected period."
    )


st.divider()


# ============================================================
# DATE-WISE MONITORING
# ============================================================

st.subheader("📆 Date-wise Monitoring")


if monitoring_rows:

    date_groups = {}

    for row in monitoring_rows:

        review_date = row[
            "Date"
        ]

        if review_date not in date_groups:

            date_groups[
                review_date
            ] = {
                "Expected": 0,
                "Submitted": 0,
                "Missing": 0,
            }

        date_groups[
            review_date
        ]["Expected"] += 1

        if row["Status"] == "Submitted":

            date_groups[
                review_date
            ]["Submitted"] += 1

        else:

            date_groups[
                review_date
            ]["Missing"] += 1


    date_rows = []

    for review_date in sorted(
        date_groups.keys()
    ):

        values = date_groups[
            review_date
        ]

        expected = values[
            "Expected"
        ]

        submitted = values[
            "Submitted"
        ]

        missing = values[
            "Missing"
        ]

        completion = (
            submitted / expected * 100
            if expected
            else 0
        )

        date_rows.append(
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
        date_rows
    )

    st.dataframe(
        date_summary_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No date-wise monitoring data available."
    )


st.divider()


# ============================================================
# TASK-WISE MONITORING
# ============================================================

st.subheader("📋 Task-wise Monitoring")


if monitoring_rows:

    task_groups = {}

    for row in monitoring_rows:

        task_key = (
            row["Task_ID"],
            row["Task_Name"],
        )

        if task_key not in task_groups:

            task_groups[
                task_key
            ] = {
                "Expected": 0,
                "Submitted": 0,
                "Missing": 0,
            }

        task_groups[
            task_key
        ]["Expected"] += 1

        if row["Status"] == "Submitted":

            task_groups[
                task_key
            ]["Submitted"] += 1

        else:

            task_groups[
                task_key
            ]["Missing"] += 1


    task_rows = []

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

        expected = values[
            "Expected"
        ]

        submitted = values[
            "Submitted"
        ]

        missing = values[
            "Missing"
        ]

        completion = (
            submitted / expected * 100
            if expected
            else 0
        )

        task_rows.append(
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
        task_rows
    )

    st.dataframe(
        task_summary_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No task-wise monitoring data available."
    )


st.divider()


# ============================================================
# MISSING / NOT REPORTING DETAILS
# ============================================================

st.subheader("🚨 Missing / Not Reporting")


missing_rows = [
    row
    for row in monitoring_rows
    if row["Status"]
    == "Missing / Not Reporting"
]


if missing_rows:

    missing_display = []

    for row in sorted(
        missing_rows,
        key=lambda x: (
            x["Date"],
            x["Coordinator_ID"],
            x["Task_Name"],
        ),
        reverse=True,
    ):

        coordinator = coordinator_lookup.get(
            row["Coordinator_ID"],
            {}
        )

        coordinator_name = (
            coordinator.get(
                "Coordinator_Name",
                coordinator.get(
                    "Name",
                    coordinator.get(
                        "Username",
                        row["Coordinator_ID"]
                    )
                )
            )
        )

        missing_display.append(
            {
                "Date": row[
                    "Date"
                ].strftime(
                    "%d-%m-%Y"
                ),
                "Coordinator ID": row[
                    "Coordinator_ID"
                ],
                "Coordinator Name": coordinator_name,
                "Task ID": row[
                    "Task_ID"
                ],
                "Task Name": row[
                    "Task_Name"
                ],
                "Assignment ID": row[
                    "Assignment_ID"
                ],
                "Status": "Missing / Not Reporting",
            }
        )


    missing_df = pd.DataFrame(
        missing_display
    )

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.success(
        "No Missing / Not Reporting Daily Reviews "
        "found for the selected period."
    )


st.divider()


# ============================================================
# DETAILED MONITORING
# ============================================================

st.subheader("🔎 Detailed Monitoring")


if monitoring_rows:

    detail_rows = []

    for row in sorted(
        monitoring_rows,
        key=lambda x: (
            x["Date"],
            x["Coordinator_ID"],
            x["Task_Name"],
        ),
        reverse=True,
    ):

        coordinator = coordinator_lookup.get(
            row["Coordinator_ID"],
            {}
        )

        coordinator_name = (
            coordinator.get(
                "Coordinator_Name",
                coordinator.get(
                    "Name",
                    coordinator.get(
                        "Username",
                        row["Coordinator_ID"]
                    )
                )
            )
        )

        detail_rows.append(
            {
                "Date": row[
                    "Date"
                ].strftime(
                    "%d-%m-%Y"
                ),
                "Coordinator": coordinator_name,
                "Coordinator ID": row[
                    "Coordinator_ID"
                ],
                "Task ID": row[
                    "Task_ID"
                ],
                "Task Name": row[
                    "Task_Name"
                ],
                "Assignment ID": row[
                    "Assignment_ID"
                ],
                "Status": row[
                    "Status"
                ],
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
        "No detailed monitoring records available."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Monitoring is calculated from ACTIVE Daily Task "
    "assignments and Daily Review records for the "
    "selected date range."
)
