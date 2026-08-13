import streamlit as st
from datetime import datetime

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
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
    page_title="Notifications",
    page_icon="🔔",
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

        if (
            value is not None
            and clean(value) != ""
        ):

            return clean(value)

    return ""


def normalize_status(status):

    status = clean(
        status
    ).lower()

    if status in [
        "completed",
        "complete",
        "done"
    ]:

        return "Completed"

    if status in [
        "in progress",
        "in-progress",
        "ongoing",
        "working"
    ]:

        return "In Progress"

    if status in [
        "pending",
        "not started",
        "not_started"
    ]:

        return "Pending"

    return clean(status).title()


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

        return []

    except Exception:

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

        assignment

        for assignment in assignments

        if get_value(
            assignment,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]


    reviews = [

        review

        for review in reviews

        if get_value(
            review,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]


# ==========================================================
# BUILD NOTIFICATIONS
# ==========================================================

notifications = []


# ==========================================================
# TASK NOTIFICATIONS
# ==========================================================

for assignment in assignments:

    status = normalize_status(
        get_value(
            assignment,
            "Status"
        )
    )

    task_id = get_value(
        assignment,
        "Task_ID",
        "Task_Id"
    )

    assignment_id = get_value(
        assignment,
        "Assignment_ID",
        "Assignment_Id"
    )

    due_date = get_value(
        assignment,
        "Due_Date",
        "Due Date"
    )

    assigned_date = get_value(
        assignment,
        "Assigned_Date",
        "Assigned Date"
    )

    priority = get_value(
        assignment,
        "Priority"
    )

    remarks = get_value(
        assignment,
        "Remarks"
    )


    if status == "Pending":

        notifications.append(
            {
                "type": "task",
                "icon": "⏳",
                "title": "Pending Task",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"is currently pending.",
                "priority": priority or "Medium",
                "date": assigned_date,
                "sort": 1
            }
        )


    elif status == "In Progress":

        notifications.append(
            {
                "type": "task",
                "icon": "🔄",
                "title": "Task In Progress",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"is currently in progress.",
                "priority": priority or "Medium",
                "date": assigned_date,
                "sort": 2
            }
        )


    if due_date:

        notifications.append(
            {
                "type": "deadline",
                "icon": "📅",
                "title": "Task Due Date",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"has due date {due_date}.",
                "priority": priority or "Medium",
                "date": due_date,
                "sort": 3
            }
        )


    if priority.lower() in [
        "high",
        "critical",
        "urgent"
    ]:

        notifications.append(
            {
                "type": "priority",
                "icon": "🚨",
                "title": "High Priority Task",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"has {priority} priority.",
                "priority": priority,
                "date": assigned_date,
                "sort": 0
            }
        )


# ==========================================================
# REVIEW NOTIFICATIONS
# ==========================================================

for review in reviews:

    review_status = normalize_status(
        get_value(
            review,
            "Status",
            "Review_Status"
        )
    )

    task_id = get_value(
        review,
        "Task_ID",
        "Task_Id"
    )

    review_date = get_value(
        review,
        "Review_Date",
        "Review Date",
        "Date"
    )

    progress = get_value(
        review,
        "Progress",
        "Progress_Update",
        "Update"
    )

    remarks = get_value(
        review,
        "Remarks",
        "Comment",
        "Comments"
    )


    if review_status == "Completed":

        notifications.append(
            {
                "type": "review",
                "icon": "✅",
                "title": "Daily Review Completed",
                "message":
                    f"Daily Review submitted for "
                    f"Task {task_id}.",
                "priority": "Normal",
                "date": review_date,
                "sort": 1
            }
        )


    elif review_status == "In Progress":

        notifications.append(
            {
                "type": "review",
                "icon": "🔄",
                "title": "Daily Review In Progress",
                "message":
                    f"Daily Review for Task {task_id} "
                    f"is marked In Progress.",
                "priority": "Normal",
                "date": review_date,
                "sort": 2
            }
        )


    elif review_status == "Pending":

        notifications.append(
            {
                "type": "review",
                "icon": "⚠️",
                "title": "Pending Daily Review",
                "message":
                    f"Daily Review for Task {task_id} "
                    f"is still pending.",
                "priority": "High",
                "date": review_date,
                "sort": 0
            }
        )


# ==========================================================
# SORT
# ==========================================================

notifications.sort(
    key=lambda x: (
        x.get(
            "sort",
            99
        ),
        x.get(
            "date",
            ""
        )
    )
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🔔 Notifications"
)

st.caption(
    f"User: {current_username} | Role: {current_role}"
)

st.divider()


# ==========================================================
# METRICS
# ==========================================================

total_notifications = len(
    notifications
)

high_priority = sum(
    1
    for notification in notifications
    if notification.get(
        "priority",
        ""
    ).lower()
    in [
        "high",
        "critical",
        "urgent"
    ]
)

task_notifications = sum(
    1
    for notification in notifications
    if notification.get(
        "type"
    )
    in [
        "task",
        "deadline",
        "priority"
    ]
)

review_notifications = sum(
    1
    for notification in notifications
    if notification.get(
        "type"
    )
    == "review"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "🔔 Total",
        total_notifications
    )


with c2:

    st.metric(
        "🚨 High Priority",
        high_priority
    )


with c3:

    st.metric(
        "📋 Task Alerts",
        task_notifications
    )


with c4:

    st.metric(
        "📝 Review Alerts",
        review_notifications
    )


st.divider()


# ==========================================================
# FILTER
# ==========================================================

st.subheader(
    "🔎 Notification Filter"
)


filter_col1, filter_col2 = st.columns(2)


with filter_col1:

    notification_filter = st.selectbox(
        "Notification Type",
        [
            "All",
            "Task",
            "Deadline",
            "Priority",
            "Review"
        ],
        key="notification_type_filter"
    )


with filter_col2:

    priority_filter = st.selectbox(
        "Priority",
        [
            "All",
            "High",
            "Critical",
            "Urgent",
            "Medium",
            "Normal",
            "Low"
        ],
        key="notification_priority_filter"
    )


filtered_notifications = []


for notification in notifications:

    ntype = notification.get(
        "type",
        ""
    )

    priority = notification.get(
        "priority",
        ""
    )


    if notification_filter != "All":

        allowed_types = {

            "Task": [
                "task"
            ],

            "Deadline": [
                "deadline"
            ],

            "Priority": [
                "priority"
            ],

            "Review": [
                "review"
            ]

        }

        if ntype not in allowed_types.get(
            notification_filter,
            []
        ):

            continue


    if priority_filter != "All":

        if priority.lower() != priority_filter.lower():

            continue


    filtered_notifications.append(
        notification
    )


# ==========================================================
# DISPLAY
# ==========================================================

st.subheader(
    "📢 Notifications"
)


if not filtered_notifications:

    st.success(
        "🎉 No notifications available."
    )

else:

    for index, notification in enumerate(
        filtered_notifications
    ):

        icon = notification.get(
            "icon",
            "🔔"
        )

        title = notification.get(
            "title",
            "Notification"
        )

        message = notification.get(
            "message",
            ""
        )

        priority = notification.get(
            "priority",
            "Normal"
        )

        date = notification.get(
            "date",
            ""
        )


        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [
                    1,
                    8
                ]
            )


            with col1:

                st.markdown(
                    f"# {icon}"
                )


            with col2:

                st.markdown(
                    f"### {title}"
                )

                st.write(
                    message
                )

                meta = (
                    f"**Priority:** {priority}"
                )

                if date:

                    meta += (
                        f"  |  **Date:** {date}"
                    )

                st.caption(
                    meta
                )


# ==========================================================
# REFRESH
# ==========================================================

st.divider()


if st.button(
    "🔄 Refresh Notifications",
    use_container_width=True,
    key="refresh_notifications"
):

    st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Notifications • Coordinator Monitoring & Task Management System"
)
