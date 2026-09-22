import streamlit as st
from datetime import datetime, date
from zoneinfo import ZoneInfo

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    NOTIFICATIONS,
    DAILY_REVIEW,
)

from services.notification_service import NotificationService
from services.task_assignment_service import TaskAssignmentService
from utils.google_sheet import read_all, update_value


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide",
)


# ============================================================
# TIMEZONE
# ============================================================

IST = ZoneInfo("Asia/Kolkata")


# ============================================================
# SESSION / LOGIN HELPERS
# ============================================================

def get_current_user():
    """
    Supports both session formats used in the project.
    """

    user = st.session_state.get("user")

    if isinstance(user, dict):
        return user

    role = st.session_state.get("role")
    user_id = st.session_state.get("user_id")
    username = st.session_state.get("username")

    if role or user_id or username:
        return {
            "Role": role,
            "User_ID": user_id,
            "Username": username,
        }

    return None


def get_user_value(user, *keys):
    """
    Safely get a value from the current user dictionary.
    """

    if not isinstance(user, dict):
        return ""

    for key in keys:
        if key in user:
            value = user.get(key)

            if value is not None and str(value).strip():
                return str(value).strip()

    return ""


current_user = get_current_user()

if not current_user:
    st.error("🔒 Please login to access Notifications.")
    st.stop()


current_role = get_user_value(
    current_user,
    "Role",
    "role",
)

current_user_id = get_user_value(
    current_user,
    "User_ID",
    "user_id",
    "UserID",
)

current_username = get_user_value(
    current_user,
    "Username",
    "username",
    "Name",
)


if current_role not in [
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
]:
    st.error("🚫 You are not authorized to access Notifications.")
    st.stop()


# ============================================================
# GENERAL HELPERS
# ============================================================

def clean(value):
    if value is None:
        return ""

    try:
        if value != value:
            return ""
    except Exception:
        pass

    return str(value).strip()


def get_value(row, *keys):
    if not isinstance(row, dict):
        return ""

    for key in keys:
        if key in row:
            value = clean(row.get(key))

            if value:
                return value

    return ""


def normalize_status(value):
    return clean(value).upper().replace("-", "_").replace(" ", "_")


def safe_read(sheet_name):
    """
    Safely read a Google Sheet.
    """

    try:
        data = read_all(sheet_name)

        if data is None:
            return []

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def parse_datetime(value):
    """
    Convert common date/datetime formats to datetime.
    """

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    text = clean(value)

    if not text:
        return None

    formats = [
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            continue

    return None


def format_datetime(value):
    dt = parse_datetime(value)

    if dt is None:
        return clean(value) or "Not Mentioned"

    return dt.strftime("%d-%m-%Y %H:%M")


def get_priority_value(row):
    return get_value(
        row,
        "Priority",
        "priority",
        "Task_Priority",
        "Task Priority",
    )


def get_task_name(row):
    return get_value(
        row,
        "Task_Name",
        "Task Name",
        "Task",
        "Title",
        "task_name",
    )


def get_task_id(row):
    return get_value(
        row,
        "Task_ID",
        "Task ID",
        "task_id",
    )


def get_coordinator_id(row):
    return get_value(
        row,
        "Coordinator_ID",
        "Coordinator ID",
        "coordinator_id",
    )


def get_assignment_id(row):
    return get_value(
        row,
        "Assignment_ID",
        "Assignment ID",
        "assignment_id",
    )


# ============================================================
# LOAD DATA
# ============================================================

assignment_service = TaskAssignmentService()

try:
    assignments = assignment_service.get_all_assignments()
except Exception:
    assignments = []

if not isinstance(assignments, list):
    assignments = []


# ------------------------------------------------------------
# IMPORTANT:
# Correct Daily Review sheet is 05_Daily_Review.
# Do NOT use 06_Daily_Review because 06 is Login History.
# ------------------------------------------------------------

reviews = safe_read(DAILY_REVIEW)

# Fallback using the exact project sheet name.
if not reviews:
    reviews = safe_read("05_Daily_Review")


# Persistent notifications
persistent_notifications = safe_read(NOTIFICATIONS)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🔔 Notifications")

st.caption(
    "View system notifications, task alerts, deadlines and Daily Review updates."
)

st.divider()


# ============================================================
# USER INFORMATION
# ============================================================

user_col1, user_col2, user_col3 = st.columns(3)

with user_col1:
    st.metric(
        "Current User",
        current_username or "Not Mentioned",
    )

with user_col2:
    st.metric(
        "Role",
        current_role or "Not Mentioned",
    )

with user_col3:
    st.metric(
        "User ID",
        current_user_id or "Not Mentioned",
    )


# ============================================================
# BUILD LIVE SYSTEM ALERTS
# ============================================================

live_alerts = []


def add_live_alert(
    alert_type,
    title,
    message,
    priority="Normal",
    created_at=None,
    task_id="",
    task_name="",
    coordinator_id="",
):
    live_alerts.append(
        {
            "Alert_Type": alert_type,
            "Title": title,
            "Message": message,
            "Priority": priority or "Normal",
            "Created_At": created_at or datetime.now(IST),
            "Task_ID": task_id,
            "Task_Name": task_name,
            "Coordinator_ID": coordinator_id,
        }
    )


# ============================================================
# TASK ALERTS
# ============================================================

for assignment in assignments:

    assignment_coordinator = get_coordinator_id(assignment)

    # Coordinator should only see own task alerts.
    if current_role == ROLE_COORDINATOR:
        if (
            assignment_coordinator
            and current_user_id
            and assignment_coordinator != current_user_id
        ):
            continue

    task_id = get_task_id(assignment)
    task_name = get_task_name(assignment)

    status = normalize_status(
        get_value(
            assignment,
            "Status",
            "Task_Status",
            "Assignment_Status",
        )
    )

    priority = get_priority_value(assignment)

    assignment_date = get_value(
        assignment,
        "Assignment_Date",
        "Assigned_Date",
        "Start_Date",
        "Date",
    )

    due_date = get_value(
        assignment,
        "Due_Date",
        "Deadline",
        "Due Date",
    )

    # --------------------------------------------------------
    # Pending Task
    # --------------------------------------------------------

    if status in [
        "PENDING",
        "ASSIGNED",
        "NOT_STARTED",
    ]:
        add_live_alert(
            alert_type="Task",
            title="📋 Pending Task",
            message=(
                f"{task_name or task_id or 'Assigned task'} "
                f"is pending."
            ),
            priority=priority or "Normal",
            created_at=assignment_date,
            task_id=task_id,
            task_name=task_name,
            coordinator_id=assignment_coordinator,
        )

    # --------------------------------------------------------
    # In Progress Task
    # --------------------------------------------------------

    if status in [
        "IN_PROGRESS",
        "INPROGRESS",
        "STARTED",
    ]:
        add_live_alert(
            alert_type="Task",
            title="🔄 Task In Progress",
            message=(
                f"{task_name or task_id or 'Assigned task'} "
                f"is currently in progress."
            ),
            priority=priority or "Normal",
            created_at=assignment_date,
            task_id=task_id,
            task_name=task_name,
            coordinator_id=assignment_coordinator,
        )

    # --------------------------------------------------------
    # High Priority
    # --------------------------------------------------------

    if normalize_status(priority) in [
        "HIGH",
        "CRITICAL",
        "URGENT",
    ]:
        add_live_alert(
            alert_type="Priority",
            title="🚨 High Priority Task",
            message=(
                f"{task_name or task_id or 'Task'} "
                f"has {priority} priority."
            ),
            priority=priority,
            created_at=assignment_date,
            task_id=task_id,
            task_name=task_name,
            coordinator_id=assignment_coordinator,
        )

    # --------------------------------------------------------
    # Due Date Alert
    # --------------------------------------------------------

    due_dt = parse_datetime(due_date)

    if due_dt is not None:

        now_ist = datetime.now(IST)

        if due_dt.tzinfo is None:
            due_dt = due_dt.replace(tzinfo=IST)

        remaining_seconds = (
            due_dt - now_ist
        ).total_seconds()

        # Due within 24 hours
        if 0 <= remaining_seconds <= 86400:

            add_live_alert(
                alert_type="Deadline",
                title="⏰ Task Due Soon",
                message=(
                    f"{task_name or task_id or 'Task'} "
                    f"is due on {due_dt.strftime('%d-%m-%Y %H:%M')}."
                ),
                priority="Urgent",
                created_at=due_dt,
                task_id=task_id,
                task_name=task_name,
                coordinator_id=assignment_coordinator,
            )

        # Already overdue
        elif remaining_seconds < 0 and status not in [
            "COMPLETED",
            "CLOSED",
            "DONE",
        ]:

            add_live_alert(
                alert_type="Deadline",
                title="🔴 Overdue Task",
                message=(
                    f"{task_name or task_id or 'Task'} "
                    f"was due on {due_dt.strftime('%d-%m-%Y %H:%M')}."
                ),
                priority="Critical",
                created_at=due_dt,
                task_id=task_id,
                task_name=task_name,
                coordinator_id=assignment_coordinator,
            )


# ============================================================
# DAILY REVIEW ALERTS
# ============================================================

for review in reviews:

    review_coordinator = get_value(
        review,
        "Coordinator_ID",
        "Coordinator ID",
        "coordinator_id",
    )

    if current_role == ROLE_COORDINATOR:

        if (
            review_coordinator
            and current_user_id
            and review_coordinator != current_user_id
        ):
            continue

    review_status = normalize_status(
        get_value(
            review,
            "Status",
            "Review_Status",
            "Review Status",
        )
    )

    review_task_id = get_task_id(review)

    review_task_name = get_value(
        review,
        "Task_Name",
        "Task Name",
        "Task",
    )

    review_date = get_value(
        review,
        "Date",
        "Review_Date",
        "Review Date",
    )

    if review_status == "COMPLETED":

        add_live_alert(
            alert_type="Review",
            title="✅ Daily Review Completed",
            message=(
                f"Daily Review completed for "
                f"{review_task_name or review_task_id or 'task'}."
            ),
            priority="Normal",
            created_at=review_date,
            task_id=review_task_id,
            task_name=review_task_name,
            coordinator_id=review_coordinator,
        )

    elif review_status in [
        "IN_PROGRESS",
        "INPROGRESS",
    ]:

        add_live_alert(
            alert_type="Review",
            title="🔄 Daily Review In Progress",
            message=(
                f"Daily Review is in progress for "
                f"{review_task_name or review_task_id or 'task'}."
            ),
            priority="Medium",
            created_at=review_date,
            task_id=review_task_id,
            task_name=review_task_name,
            coordinator_id=review_coordinator,
        )

    elif review_status in [
        "PENDING",
        "NOT_STARTED",
        "MISSING",
        "NOT_REPORTING",
    ]:

        add_live_alert(
            alert_type="Review",
            title="⚠️ Pending Daily Review",
            message=(
                f"Daily Review is pending for "
                f"{review_task_name or review_task_id or 'task'}."
            ),
            priority="High",
            created_at=review_date,
            task_id=review_task_id,
            task_name=review_task_name,
            coordinator_id=review_coordinator,
        )


# ============================================================
# PERSISTENT NOTIFICATIONS FILTER
# ============================================================

visible_notifications = []

for row_index, notification in enumerate(
    persistent_notifications,
    start=2,
):

    recipient_id = get_value(
        notification,
        "Recipient_ID",
        "Recipient ID",
        "recipient_id",
    )

    if current_role in [
        ROLE_DEVELOPER,
        ROLE_ADMIN,
    ]:
        visible = True

    else:
        visible = (
            recipient_id == current_user_id
            or recipient_id == current_username
        )

    if not visible:
        continue

    item = dict(notification)

    # Preserve actual Google Sheet row number.
    item["_sheet_row"] = row_index

    visible_notifications.append(item)


# ============================================================
# NOTIFICATION COUNTS
# ============================================================

unread_notifications = [
    item
    for item in visible_notifications
    if normalize_status(
        get_value(
            item,
            "Status",
            "Notification_Status",
        )
    ) == "UNREAD"
]


unread_count = len(unread_notifications)


metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "🔔 Notifications",
        len(visible_notifications),
    )

with metric2:
    st.metric(
        "📩 Unread",
        unread_count,
    )

with metric3:
    st.metric(
        "⚡ Live Alerts",
        len(live_alerts),
    )


st.divider()


# ============================================================
# MARK ALL AS READ
# ============================================================

if unread_notifications:

    if st.button(
        "✅ Mark All Notifications as Read",
        use_container_width=True,
    ):

        updated = 0

        for notification in unread_notifications:

            sheet_row = notification.get("_sheet_row")

            if not sheet_row:
                continue

            try:
                update_value(
                    NOTIFICATIONS,
                    sheet_row,
                    6,
                    "READ",
                )

                updated += 1

            except Exception:
                continue

        st.success(
            f"✅ {updated} notification(s) marked as read."
        )

        st.rerun()

else:

    st.info("📭 No unread notifications.")


# ============================================================
# PERSISTENT NOTIFICATIONS
# ============================================================

st.subheader("📩 Persistent Notifications")

if not visible_notifications:

    st.info(
        "No persistent notifications are available for the current user."
    )

else:

    for notification in reversed(visible_notifications):

        title = get_value(
            notification,
            "Title",
        )

        message = get_value(
            notification,
            "Message",
        )

        notification_type = get_value(
            notification,
            "Type",
            "Notification_Type",
        )

        status = normalize_status(
            get_value(
                notification,
                "Status",
            )
        )

        created_at = get_value(
            notification,
            "Created_At",
            "Created At",
            "Date",
        )

        sheet_row = notification.get("_sheet_row")

        if status == "UNREAD":

            status_text = "🔵 UNREAD"

        else:

            status_text = "⚪ READ"

        with st.container(border=True):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.markdown(
                    f"### {title or 'Notification'}"
                )

                st.write(
                    message or "No message available."
                )

                info_parts = []

                if notification_type:
                    info_parts.append(
                        f"**Type:** {notification_type}"
                    )

                if created_at:
                    info_parts.append(
                        f"**Created:** {format_datetime(created_at)}"
                    )

                info_parts.append(
                    f"**Status:** {status_text}"
                )

                st.caption(
                    " | ".join(info_parts)
                )

            with col2:

                if status == "UNREAD":

                    if st.button(
                        "✓ Read",
                        key=f"read_notification_{sheet_row}",
                        use_container_width=True,
                    ):

                        try:

                            update_value(
                                NOTIFICATIONS,
                                sheet_row,
                                6,
                                "READ",
                            )

                            st.success(
                                "Marked as read."
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(
                                f"Unable to update notification: {exc}"
                            )


# ============================================================
# LIVE SYSTEM ALERTS
# ============================================================

st.divider()

st.subheader("⚡ Live System Alerts")

if not live_alerts:

    st.success(
        "🎉 No active task or Daily Review alerts."
    )

else:

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        alert_type_filter = st.selectbox(
            "Notification Type",
            [
                "All",
                "Task",
                "Deadline",
                "Priority",
                "Review",
            ],
            key="notification_type_filter",
        )

    with filter_col2:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "Critical",
                "Urgent",
                "High",
                "Medium",
                "Normal",
                "Low",
            ],
            key="notification_priority_filter",
        )


    filtered_alerts = []

    for alert in live_alerts:

        if (
            alert_type_filter != "All"
            and alert.get("Alert_Type")
            != alert_type_filter
        ):
            continue

        if priority_filter != "All":

            if normalize_status(
                alert.get("Priority")
            ) != normalize_status(
                priority_filter
            ):
                continue

        filtered_alerts.append(alert)


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    def alert_sort_key(alert):

        dt = parse_datetime(
            alert.get("Created_At")
        )

        if dt is None:
            return datetime.min.replace(
                tzinfo=IST
            )

        if dt.tzinfo is None:
            dt = dt.replace(
                tzinfo=IST
            )

        return dt


    filtered_alerts.sort(
        key=alert_sort_key,
        reverse=True,
    )


    if not filtered_alerts:

        st.info(
            "No live alerts match the selected filters."
        )

    else:

        for alert in filtered_alerts:

            priority = normalize_status(
                alert.get("Priority")
            )

            if priority == "CRITICAL":

                icon = "🔴"

            elif priority == "URGENT":

                icon = "🟠"

            elif priority == "HIGH":

                icon = "🟡"

            elif priority == "MEDIUM":

                icon = "🔵"

            else:

                icon = "⚪"


            title = alert.get(
                "Title",
                "System Alert",
            )

            message = alert.get(
                "Message",
                "",
            )

            created_at = alert.get(
                "Created_At"
            )

            task_name = alert.get(
                "Task_Name",
                "",
            )

            task_id = alert.get(
                "Task_ID",
                "",
            )

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### {icon} {title}"
                )

                st.write(message)

                detail_parts = []

                if priority:
                    detail_parts.append(
                        f"**Priority:** {priority.title()}"
                    )

                if alert.get("Alert_Type"):
                    detail_parts.append(
                        f"**Type:** {alert.get('Alert_Type')}"
                    )

                if task_name:
                    detail_parts.append(
                        f"**Task:** {task_name}"
                    )

                elif task_id:
                    detail_parts.append(
                        f"**Task ID:** {task_id}"
                    )

                if created_at:
                    detail_parts.append(
                        f"**Date:** {format_datetime(created_at)}"
                    )

                if detail_parts:

                    st.caption(
                        " | ".join(detail_parts)
                    )


# ============================================================
# REFRESH
# ============================================================

st.divider()

refresh_col1, refresh_col2 = st.columns(
    [1, 5]
)

with refresh_col1:

    if st.button(
        "🔄 Refresh",
        use_container_width=True,
    ):

        st.rerun()

with refresh_col2:

    st.caption(
        "Notifications and live alerts are loaded from the configured Google Sheets."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    f"MSU/EPID Health Coordinator Monitoring System • "
    f"Notifications • "
    f"{datetime.now(IST).strftime('%d-%m-%Y %H:%M')}"
)
