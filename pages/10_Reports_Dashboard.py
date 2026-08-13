import streamlit as st
import pandas as pd

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)

from services.task_assignment_service import (
    TaskAssignmentService
)

try:
    from services.daily_review_service import (
        DailyReviewService
    )
except Exception:
    DailyReviewService = None


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Reports Dashboard",
    page_icon="📊",
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

current_role = str(
    st.session_state.get(
        "role",
        ""
    )
).strip()

current_user_id = str(
    st.session_state.get(
        "user_id",
        ""
    )
).strip()

current_username = str(
    st.session_state.get(
        "username",
        ""
    )
).strip()


# ==========================================================
# HELPERS
# ==========================================================

def clean(value):

    if value is None:
        return ""

    return str(value).strip()


def get_value(row, *keys):

    if not row:
        return ""

    for key in keys:

        value = row.get(
            key,
            ""
        )

        if value is not None:

            value = clean(value)

            if value != "":
                return value

    return ""


def normalize_status(value):

    value = clean(value).lower()

    if value in [
        "completed",
        "complete",
        "done"
    ]:
        return "Completed"

    if value in [
        "in progress",
        "in-progress",
        "ongoing",
        "working"
    ]:
        return "In Progress"

    if value in [
        "pending",
        "not started",
        "not_started"
    ]:
        return "Pending"

    return clean(value).title()


def load_assignments():

    try:

        return (
            TaskAssignmentService
            .get_all_assignments()
            or []
        )

    except Exception:

        return []


def load_reviews():

    if DailyReviewService is None:
        return []

    try:

        if hasattr(
            DailyReviewService,
            "get_all_reviews"
        ):

            return (
                DailyReviewService
                .get_all_reviews()
                or []
            )

        if hasattr(
            DailyReviewService,
            "get_all"
        ):

            return (
                DailyReviewService
                .get_all()
                or []
            )

    except Exception:
        pass

    return []


# ==========================================================
# LOAD DATA
# ==========================================================

assignments = load_assignments()

reviews = load_reviews()


# ==========================================================
# ROLE FILTER
# ==========================================================

if current_role.lower() == "coordinator":

    assignments = [

        row

        for row in assignments

        if get_value(
            row,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]

    reviews = [

        row

        for row in reviews

        if get_value(
            row,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]


# ==========================================================
# ACTIVE ASSIGNMENTS
# ==========================================================

active_assignments = [

    row

    for row in assignments

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    not in [
        "Removed",
        "Deleted",
        "Inactive"
    ]

]


# ==========================================================
# TASK STATUS COUNTS
# ==========================================================

total_tasks = len(
    active_assignments
)

pending_tasks = sum(

    1

    for row in active_assignments

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    == "Pending"

)

in_progress_tasks = sum(

    1

    for row in active_assignments

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    == "In Progress"

)

completed_tasks = sum(

    1

    for row in active_assignments

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    == "Completed"

)


if total_tasks:

    completion_percentage = (
        completed_tasks
        / total_tasks
        * 100
    )

else:

    completion_percentage = 0


# ==========================================================
# REVIEW COUNTS
# ==========================================================

total_reviews = len(
    reviews
)

completed_reviews = sum(

    1

    for row in reviews

    if normalize_status(
        get_value(
            row,
            "Status",
            "Review_Status"
        )
    )
    == "Completed"

)

pending_reviews = sum(

    1

    for row in reviews

    if normalize_status(
        get_value(
            row,
            "Status",
            "Review_Status"
        )
    )
    == "Pending"

)

in_progress_reviews = sum(

    1

    for row in reviews

    if normalize_status(
        get_value(
            row,
            "Status",
            "Review_Status"
        )
    )
    == "In Progress"

)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "📊 Reports Dashboard"
)

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )


with c2:

    st.metric(
        "⏳ Pending",
        pending_tasks
    )


with c3:

    st.metric(
        "🔄 In Progress",
        in_progress_tasks
    )


with c4:

    st.metric(
        "✅ Completed",
        completed_tasks
    )


with c5:

    st.metric(
        "📈 Completion",
        f"{completion_percentage:.1f}%"
    )


st.divider()


# ==========================================================
# TASK STATUS
# ==========================================================

st.subheader(
    "📊 Task Status"
)


task_chart = pd.DataFrame(
    {
        "Status": [
            "Pending",
            "In Progress",
            "Completed"
        ],
        "Count": [
            pending_tasks,
            in_progress_tasks,
            completed_tasks
        ]
    }
)


if total_tasks:

    st.bar_chart(
        task_chart.set_index(
            "Status"
        ),
        use_container_width=True
    )

else:

    st.info(
        "No task assignment data available."
    )


st.divider()


# ==========================================================
# DAILY REVIEW SUMMARY
# ==========================================================

st.subheader(
    "📝 Daily Review Summary"
)


r1, r2, r3, r4 = st.columns(4)


with r1:

    st.metric(
        "Total Reviews",
        total_reviews
    )


with r2:

    st.metric(
        "Pending Reviews",
        pending_reviews
    )


with r3:

    st.metric(
        "In Progress",
        in_progress_reviews
    )


with r4:

    st.metric(
        "Completed Reviews",
        completed_reviews
    )


review_chart = pd.DataFrame(
    {
        "Status": [
            "Pending",
            "In Progress",
            "Completed"
        ],
        "Count": [
            pending_reviews,
            in_progress_reviews,
            completed_reviews
        ]
    }
)


if total_reviews:

    st.bar_chart(
        review_chart.set_index(
            "Status"
        ),
        use_container_width=True
    )

else:

    st.info(
        "No Daily Review submissions available."
    )


st.divider()


# ==========================================================
# ASSIGNMENT TABLE
# ==========================================================

st.subheader(
    "📋 Assignment Details"
)


assignment_rows = []


for row in active_assignments:

    assignment_rows.append(
        {
            "Assignment ID":
                get_value(
                    row,
                    "Assignment_ID",
                    "Assignment_Id"
                ),

            "Coordinator ID":
                get_value(
                    row,
                    "Coordinator_ID",
                    "Coordinator_Id"
                ),

            "Task ID":
                get_value(
                    row,
                    "Task_ID",
                    "Task_Id"
                ),

            "Assigned By":
                get_value(
                    row,
                    "Assigned_By",
                    "AssignedBy"
                ),

            "Assigned Date":
                get_value(
                    row,
                    "Assigned_Date",
                    "Assigned Date"
                ),

            "Due Date":
                get_value(
                    row,
                    "Due_Date",
                    "Due Date"
                ),

            "Priority":
                get_value(
                    row,
                    "Priority"
                ),

            "Status":
                normalize_status(
                    get_value(
                        row,
                        "Status"
                    )
                ),

            "Remarks":
                get_value(
                    row,
                    "Remarks"
                )
        }
    )


if assignment_rows:

    assignment_df = pd.DataFrame(
        assignment_rows
    )

    st.dataframe(
        assignment_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No assignments available."
    )


st.divider()


# ==========================================================
# DAILY REVIEW TABLE
# ==========================================================

st.subheader(
    "📝 Daily Review Details"
)


review_rows = []


for row in reviews:

    review_rows.append(
        {
            "Review Date":
                get_value(
                    row,
                    "Review_Date",
                    "Review Date",
                    "Date"
                ),

            "Coordinator ID":
                get_value(
                    row,
                    "Coordinator_ID",
                    "Coordinator_Id"
                ),

            "Task ID":
                get_value(
                    row,
                    "Task_ID",
                    "Task_Id"
                ),

            "Status":
                normalize_status(
                    get_value(
                        row,
                        "Status",
                        "Review_Status"
                    )
                ),

            "Progress":
                get_value(
                    row,
                    "Progress",
                    "Progress_Update",
                    "Update"
                ),

            "Remarks":
                get_value(
                    row,
                    "Remarks",
                    "Comment",
                    "Comments"
                )
        }
    )


if review_rows:

    review_df = pd.DataFrame(
        review_rows
    )

    st.dataframe(
        review_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No Daily Review data available."
    )


st.divider()


# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.subheader(
    "📥 Download Report"
)


if assignment_rows:

    csv_data = pd.DataFrame(
        assignment_rows
    ).to_csv(
        index=False
    ).encode(
        "utf-8"
    )


    st.download_button(
        "📥 Download Task Report",
        data=csv_data,
        file_name="Task_Monitoring_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


if review_rows:

    review_csv = pd.DataFrame(
        review_rows
    ).to_csv(
        index=False
    ).encode(
        "utf-8"
    )


    st.download_button(
        "📥 Download Daily Review Report",
        data=review_csv,
        file_name="Daily_Review_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==========================================================
# REFRESH
# ==========================================================

st.divider()


if st.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):

    st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Reports Dashboard • Coordinator Monitoring & Task Management System"
)
