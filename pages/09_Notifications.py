import streamlit as st
import pandas as pd

from core.navigation import require_login

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    NOTIFICATIONS
)

from services.notification_service import (
    NotificationService
)

from utils.google_sheet import (
    read_all
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
# LOGIN / ACCESS
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

    value = clean(value).upper()

    if value == "UNREAD":
        return "UNREAD"

    if value == "READ":
        return "READ"

    return value


# ==========================================================
# LOAD NOTIFICATIONS
# ==========================================================

def load_notifications():

    try:

        data = read_all(
            NOTIFICATIONS
        )

        return data if data else []

    except Exception:

        return []


# ==========================================================
# LOAD DATA
# ==========================================================

all_notifications = load_notifications()


# ==========================================================
# ROLE / USER FILTER
# ==========================================================

notifications = [

    row

    for row in all_notifications

    if get_value(
        row,
        "Recipient_ID",
        "Recipient_Id",
        "Recipient"
    )
    == current_user_id

]


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title(
    "🔔 Notifications"
)

st.caption(
    "View your system notifications and alerts."
)


if current_username:

    st.write(
        f"👤 **User:** {current_username}"
    )


if current_role:

    st.write(
        f"🔐 **Role:** {current_role}"
    )

if current_user_id:

    st.write(
        f"🆔 **User ID:** {current_user_id}"
    )


st.divider()


# ==========================================================
# SUMMARY
# ==========================================================

unread_notifications = [

    row

    for row in notifications

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    == "UNREAD"

]

read_notifications = [

    row

    for row in notifications

    if normalize_status(
        get_value(
            row,
            "Status"
        )
    )
    == "READ"

]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔔 Total Notifications",
        len(notifications)
    )


with col2:

    st.metric(
        "🆕 Unread",
        len(unread_notifications)
    )


with col3:

    st.metric(
        "✓ Read",
        len(read_notifications)
    )


st.divider()


# ==========================================================
# UNREAD NOTIFICATIONS
# ==========================================================

st.subheader(
    "🆕 Unread Notifications"
)


if unread_notifications:

    for index, notification in enumerate(
        unread_notifications
    ):

        notification_id = get_value(
            notification,
            "Notification_ID",
            "Notification_Id",
            "ID"
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

        created_at = get_value(
            notification,
            "Created_At",
            "Created At",
            "Date"
        )

        st.markdown(
            f"""
            ### 🔔 {title}

            **Type:** {notification_type}

            **Message:** {message}

            **Created:** {created_at}
            """
        )

        col_a, col_b = st.columns(
            [5, 1]
        )

        with col_a:

            st.caption(
                f"Notification ID: {notification_id}"
            )

        with col_b:

            mark_key = (
                "mark_read_"
                + str(notification_id)
                + "_"
                + str(index)
            )

            if st.button(
                "✓ Mark as Read",
                key=mark_key,
                use_container_width=True
            ):

                try:

                    # --------------------------------------------------
                    # Find actual Google Sheet row
                    #
                    # read_all() does not provide row numbers.
                    # Header = row 1
                    # First data row = row 2
                    # --------------------------------------------------

                    actual_row = None

                    for sheet_index, sheet_row in enumerate(
                        all_notifications,
                        start=2
                    ):

                        sheet_notification_id = get_value(
                            sheet_row,
                            "Notification_ID",
                            "Notification_Id",
                            "ID"
                        )

                        sheet_recipient_id = get_value(
                            sheet_row,
                            "Recipient_ID",
                            "Recipient_Id",
                            "Recipient"
                        )

                        if (
                            sheet_notification_id
                            == notification_id

                            and

                            sheet_recipient_id
                            == current_user_id
                        ):

                            actual_row = sheet_index

                            break


                    if actual_row is not None:

                        NotificationService.mark_as_read(
                            actual_row
                        )

                        st.success(
                            "Notification marked as read."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Notification row could not be found."
                        )

                except Exception as e:

                    st.error(
                        f"Unable to mark notification as read: {e}"
                    )


        st.divider()


else:

    st.success(
        "✅ No unread notifications."
    )


# ==========================================================
# READ NOTIFICATIONS
# ==========================================================

st.subheader(
    "✓ Read Notifications"
)


if read_notifications:

    read_rows = []

    for notification in read_notifications:

        read_rows.append(
            {
                "Notification ID":
                    get_value(
                        notification,
                        "Notification_ID",
                        "Notification_Id",
                        "ID"
                    ),

                "Title":
                    get_value(
                        notification,
                        "Title"
                    ),

                "Message":
                    get_value(
                        notification,
                        "Message"
                    ),

                "Type":
                    get_value(
                        notification,
                        "Type"
                    ),

                "Status":
                    get_value(
                        notification,
                        "Status"
                    ),

                "Created At":
                    get_value(
                        notification,
                        "Created_At",
                        "Created At",
                        "Date"
                    )
            }
        )


    read_df = pd.DataFrame(
        read_rows
    )


    st.dataframe(
        read_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No read notifications available."
    )


# ==========================================================
# REFRESH
# ==========================================================

st.divider()


if st.button(
    "🔄 Refresh Notifications",
    use_container_width=True
):

    st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Notifications • MSU/EPID Health Coordinator Monitoring System"
)
