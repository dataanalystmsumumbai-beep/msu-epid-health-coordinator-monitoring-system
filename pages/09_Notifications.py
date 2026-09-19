import streamlit as st
import pandas as pd

from datetime import datetime
from zoneinfo import ZoneInfo

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    NOTIFICATIONS,
)

from services.task_assignment_service import (
    TaskAssignmentService
)

from utils.google_sheet import (
    read_all,
    update_value,
)


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
# INDIA TIMEZONE
# ==========================================================

INDIA_TZ = ZoneInfo(
    "Asia/Kolkata"
)


# ==========================================================
# SESSION
# ==========================================================

current_user = st.session_state.get(
    "user",
    {}
)

current_user_id = str(
    st.session_state.get(
        "user_id",
        current_user.get(
            "User_ID",
            ""
        )
    )
).strip()

current_username = str(
    st.session_state.get(
        "username",
        current_user.get(
            "Username",
            ""
        )
    )
).strip()

current_role = str(
    st.session_state.get(
        "role",
        current_user.get(
            "Role",
            ""
        )
    )
).strip()


# ==========================================================
# HELPERS
# ==========================================================

def clean(value):

    if value is None:
        return ""

    return str(
        value
    ).strip()


def get_value(
    row,
    *keys
):

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


def normalize_status(
    status
):

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

    return clean(
        status
    ).title()


def safe_read(
    sheet_name
):

    try:

        data = read_all(
            sheet_name
        )

        return (
            data
            if data
            else []
        )

    except Exception:

        return []


# ==========================================================
# LOAD CURRENT DATA
# ==========================================================

assignments = []

try:

    assignments = (
        TaskAssignmentService
        .get_all_assignments()
        or []
    )

except Exception:

    assignments = []


# ==========================================================
# LOAD DAILY REVIEWS
# ==========================================================

reviews = safe_read(
    "06_Daily_Review"
)

# Fallback for projects where the configured
# Daily Review constant is different.

if not reviews:

    try:

        from config.config import DAILY_REVIEW

        reviews = safe_read(
            DAILY_REVIEW
        )

    except Exception:

        reviews = []


# ==========================================================
# LOAD PERSISTENT NOTIFICATIONS
# ==========================================================

persistent_notifications = safe_read(
    NOTIFICATIONS
)


# ==========================================================
# ROLE FILTER FOR DYNAMIC ALERTS
# ==========================================================

dynamic_assignments = list(
    assignments
)

dynamic_reviews = list(
    reviews
)


if current_role.lower() == "coordinator":

    dynamic_assignments = [

        assignment

        for assignment in dynamic_assignments

        if get_value(
            assignment,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]


    dynamic_reviews = [

        review

        for review in dynamic_reviews

        if get_value(
            review,
            "Coordinator_ID",
            "Coordinator_Id"
        )
        == current_user_id

    ]


# ==========================================================
# BUILD DYNAMIC NOTIFICATIONS
# ==========================================================

dynamic_notifications = []


# ==========================================================
# TASK NOTIFICATIONS
# ==========================================================

for assignment in dynamic_assignments:

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


    if status == "Pending":

        dynamic_notifications.append(
            {
                "type": "task",
                "icon": "⏳",
                "title": "Pending Task",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"is currently pending.",
                "priority":
                    priority or "Medium",
                "date":
                    assigned_date,
                "sort": 1
            }
        )


    elif status == "In Progress":

        dynamic_notifications.append(
            {
                "type": "task",
                "icon": "🔄",
                "title": "Task In Progress",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"is currently in progress.",
                "priority":
                    priority or "Medium",
                "date":
                    assigned_date,
                "sort": 2
            }
        )


    if due_date:

        dynamic_notifications.append(
            {
                "type": "deadline",
                "icon": "📅",
                "title": "Task Due Date",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"has due date {due_date}.",
                "priority":
                    priority or "Medium",
                "date":
                    due_date,
                "sort": 3
            }
        )


    if priority.lower() in [
        "high",
        "critical",
        "urgent"
    ]:

        dynamic_notifications.append(
            {
                "type": "priority",
                "icon": "🚨",
                "title": "High Priority Task",
                "message":
                    f"Task {task_id or assignment_id} "
                    f"has {priority} priority.",
                "priority":
                    priority,
                "date":
                    assigned_date,
                "sort": 0
            }
        )


# ==========================================================
# REVIEW NOTIFICATIONS
# ==========================================================

for review in dynamic_reviews:

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


    if review_status == "Completed":

        dynamic_notifications.append(
            {
                "type": "review",
                "icon": "✅",
                "title": "Daily Review Completed",
                "message":
                    f"Daily Review submitted for "
                    f"Task {task_id}.",
                "priority": "Normal",
                "date":
                    review_date,
                "sort": 1
            }
        )


    elif review_status == "In Progress":

        dynamic_notifications.append(
            {
                "type": "review",
                "icon": "🔄",
                "title": "Daily Review In Progress",
                "message":
                    f"Daily Review for Task {task_id} "
                    f"is marked In Progress.",
                "priority": "Normal",
                "date":
                    review_date,
                "sort": 2
            }
        )


    elif review_status == "Pending":

        dynamic_notifications.append(
            {
                "type": "review",
                "icon": "⚠️",
                "title": "Pending Daily Review",
                "message":
                    f"Daily Review for Task {task_id} "
                    f"is still pending.",
                "priority": "High",
                "date":
                    review_date,
                "sort": 0
            }
        )


# ==========================================================
# PERSISTENT USER NOTIFICATIONS
# ==========================================================

user_notifications = []


for index, notification in enumerate(
    persistent_notifications
):

    recipient_id = get_value(
        notification,
        "Recipient_ID",
        "Recipient_Id"
    )

    if current_role.lower() in [
        "admin",
        "developer"
    ]:

        visible = True

    else:

        visible = (
            recipient_id
            == current_user_id
        )


    if not visible:

        continue


    user_notifications.append(
        {
            "sheet_row": index + 2,
            "notification": notification
        }
    )


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🔔 Notifications"
)

st.caption(
    f"User: {current_username} | "
    f"Role: {current_role}"
)

st.divider()


# ==========================================================
# PERSISTENT NOTIFICATION SUMMARY
# ==========================================================

persistent_total = len(
    user_notifications
)

persistent_unread = sum(
    1
    for item in user_notifications

    if get_value(
        item["notification"],
        "Status"
    ).upper()
    == "UNREAD"
)

persistent_read = (
    persistent_total
    - persistent_unread
)


# ==========================================================
# DYNAMIC SUMMARY
# ==========================================================

dynamic_total = len(
    dynamic_notifications
)

high_priority = sum(
    1
    for notification
    in dynamic_notifications

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


# ==========================================================
# METRICS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "🔔 Notifications",
        persistent_total
    )


with c2:

    st.metric(
        "🟠 Unread",
        persistent_unread
    )


with c3:

    st.metric(
        "📢 Live Alerts",
        dynamic_total
    )


with c4:

    st.metric(
        "🚨 High Priority",
        high_priority
    )


st.divider()


# ==========================================================
# MARK ALL AS READ
# ==========================================================

if persistent_unread > 0:

    if st.button(
        "✓ Mark All Notifications as Read",
        use_container_width=True,
        key="mark_all_notifications_read"
    ):

        updated = 0

        for item in user_notifications:

            notification = item[
                "notification"
            ]

            row_number = item[
                "sheet_row"
            ]

            status = get_value(
                notification,
                "Status"
            ).upper()

            if status != "UNREAD":

                continue

            try:

                update_value(
                    NOTIFICATIONS,
                    row_number,
                    6,
                    "READ"
                )

                updated += 1

            except Exception:

                pass


        st.success(
            f"{updated} notification(s) "
            "marked as read."
        )

        st.rerun()


# ==========================================================
# PERSISTENT NOTIFICATIONS
# ==========================================================

st.subheader(
    "📬 My Notifications"
)


if not user_notifications:

    st.info(
        "No persistent notifications found."
    )

else:

    for item in reversed(
        user_notifications
    ):

        notification = item[
            "notification"
        ]

        row_number = item[
            "sheet_row"
        ]

        notification_id = get_value(
            notification,
            "Notification_ID",
            "Notification_Id"
        )

        title = get_value(
            notification,
            "Title"
        )

        message = get_value(
            notification,
            "Message"
        )

        notification_type = get_value(
            notification,
            "Type"
        )

        status = get_value(
            notification,
            "Status"
        ).upper()

        created_at = get_value(
            notification,
            "Created_At",
            "Created At"
        )


        is_unread = (
            status == "UNREAD"
        )


        if is_unread:

            icon = "🟠"

        else:

            icon = "🟢"


        with st.container(
            border=True
        ):

            left, right = st.columns(
                [7, 1]
            )


            with left:

                st.markdown(
                    f"### {icon} {title or 'Notification'}"
                )

                if message:

                    st.write(
                        message
                    )

                meta = []

                if notification_type:

                    meta.append(
                        f"Type: {notification_type}"
                    )

                if created_at:

                    meta.append(
                        f"Created: {created_at}"
                    )

                if meta:

                    st.caption(
                        " | ".join(meta)
                    )


            with right:

                if is_unread:

                    st.caption(
                        "UNREAD"
                    )

                    if st.button(
                        "✓ Read",
                        key=(
                            f"read_notification_"
                            f"{row_number}_"
                            f"{notification_id}"
                        ),
                        use_container_width=True,
                    ):

                        try:

                            update_value(
                                NOTIFICATIONS,
                                row_number,
                                6,
                                "READ"
                            )

                            st.success(
                                "Marked as read."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Unable to update: {e}"
                            )

                else:

                    st.caption(
                        "READ"
                    )


st.divider()


# ==========================================================
# LIVE SYSTEM ALERTS
# ==========================================================

st.subheader(
    "📢 Live System Alerts"
)

st.caption(
    "These alerts are generated from current "
    "task assignments and Daily Review records."
)


# ==========================================================
# FILTERS
# ==========================================================

filter_col1, filter_col2 = st.columns(
    2
)


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
        key="live_notification_type_filter"
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
        key="live_notification_priority_filter"
    )


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_dynamic = []


for notification
in dynamic_notifications:

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

        if (
            priority.lower()
            !=
            priority_filter.lower()
        ):

            continue


    filtered_dynamic.append(
        notification
    )


# ==========================================================
# SORT
# ==========================================================

filtered_dynamic.sort(
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
# DISPLAY LIVE ALERTS
# ==========================================================

if not filtered_dynamic:

    st.success(
        "🎉 No live alerts available."
    )

else:

    for notification
    in filtered_dynamic:

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

        alert_date = notification.get(
            "date",
            ""
        )


        with st.container(
            border=True
        ):

            st.markdown(
                f"### {icon} {title}"
            )

            st.write(
                message
            )

            meta = (
                f"**Priority:** {priority}"
            )

            if alert_date:

                meta += (
                    f" | **Date:** {alert_date}"
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
    "MSU / EPID Health Coordinator Monitoring System "
    "| Notifications"
)
