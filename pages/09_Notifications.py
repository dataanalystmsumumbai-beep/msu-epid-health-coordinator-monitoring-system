import streamlit as st

from config.config import (
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR,
    NOTIFICATIONS
)

from utils.google_sheet import (
    read_all,
    update_value
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Notifications",
    page_icon="🔔",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):

    st.error("Please login first.")
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
        "User_ID",
        current_user.get(
            "Coordinator_ID",
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
# HEADER
# ==========================================================

st.title(
    "🔔 Notifications"
)

st.caption(
    f"Welcome, {current_username}"
)

st.divider()


# ==========================================================
# LOAD NOTIFICATIONS
# ==========================================================

try:

    notifications = read_all(
        NOTIFICATIONS
    )

except Exception as e:

    st.error(
        f"Unable to load notifications: {e}"
    )

    notifications = []


# ==========================================================
# HELPER
# ==========================================================

def normalize(value):

    return str(
        value if value is not None else ""
    ).strip()


# ==========================================================
# FILTER USER NOTIFICATIONS
# ==========================================================

visible_notifications = []


for row_number, notification in enumerate(
    notifications,
    start=2
):

    target_user_id = normalize(
        notification.get(
            "User_ID",
            notification.get(
                "User_Id",
                notification.get(
                    "Coordinator_ID",
                    ""
                )
            )
        )
    )

    target_username = normalize(
        notification.get(
            "Username",
            ""
        )
    )


    target_role = normalize(
        notification.get(
            "Role",
            ""
        )
    )


    # ------------------------------------------------------
    # ADMIN / DEVELOPER BROAD NOTIFICATIONS
    # ------------------------------------------------------

    is_global = target_user_id == "" and target_username == ""


    # ------------------------------------------------------
    # USER MATCH
    # ------------------------------------------------------

    user_match = (

        target_user_id
        and target_user_id == current_user_id

    ) or (

        target_username
        and target_username.lower()
        == current_username.lower()

    )


    # ------------------------------------------------------
    # ROLE MATCH
    # ------------------------------------------------------

    role_match = (

        target_role
        and target_role.upper()
        == current_role.upper()

    )


    if (
        is_global
        or user_match
        or role_match
    ):

        visible_notifications.append(
            (
                row_number,
                notification
            )
        )


# ==========================================================
# COUNTS
# ==========================================================

unread_notifications = []

for row_number, notification in visible_notifications:

    read_status = normalize(
        notification.get(
            "Read",
            notification.get(
                "Is_Read",
                notification.get(
                    "Status",
                    ""
                )
            )
        )
    ).upper()

    if read_status not in [
        "YES",
        "READ",
        "TRUE"
    ]:

        unread_notifications.append(
            (
                row_number,
                notification
            )
        )


# ==========================================================
# SUMMARY
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "🔔 Total Notifications",
        len(
            visible_notifications
        )
    )

with c2:

    st.metric(
        "🟠 Unread",
        len(
            unread_notifications
        )
    )

with c3:

    st.metric(
        "⚪ Read",
        len(
            visible_notifications
        )
        - len(
            unread_notifications
        )
    )


st.divider()


# ==========================================================
# MARK ALL AS READ
# ==========================================================

if unread_notifications:

    if st.button(
        "✅ Mark All as Read",
        use_container_width=True,
        key="mark_all_notifications_read"
    ):

        success_count = 0

        for row_number, notification in unread_notifications:

            try:

                # Expected Read column = 8
                update_value(
                    NOTIFICATIONS,
                    row_number,
                    8,
                    "YES"
                )

                success_count += 1

            except Exception:
                pass


        if success_count:

            st.success(
                f"{success_count} notification(s) marked as read."
            )

            st.rerun()

        else:

            st.error(
                "Unable to update notifications."
            )


# ==========================================================
# NOTIFICATION LIST
# ==========================================================

if not visible_notifications:

    st.info(
        "🎉 No notifications available."
    )

else:

    # Show newest records first
    ordered_notifications = list(
        reversed(
            visible_notifications
        )
    )


    for index, (
        row_number,
        notification
    ) in enumerate(
        ordered_notifications
    ):

        title = normalize(
            notification.get(
                "Title",
                notification.get(
                    "Notification_Title",
                    "Notification"
                )
            )
        )


        message = normalize(
            notification.get(
                "Message",
                notification.get(
                    "Notification",
                    notification.get(
                        "Description",
                        ""
                    )
                )
            )
        )


        notification_type = normalize(
            notification.get(
                "Type",
                notification.get(
                    "Notification_Type",
                    "INFO"
                )
            )
        ).upper()


        created_at = normalize(
            notification.get(
                "Created_At",
                notification.get(
                    "CreatedAt",
                    notification.get(
                        "Date",
                        ""
                    )
                )
            )
        )


        read_status = normalize(
            notification.get(
                "Read",
                notification.get(
                    "Is_Read",
                    notification.get(
                        "Status",
                        ""
                    )
                )
            )
        ).upper()


        is_read = read_status in [
            "YES",
            "READ",
            "TRUE"
        ]


        # --------------------------------------------------
        # TYPE ICON
        # --------------------------------------------------

        if notification_type in [
            "SUCCESS",
            "COMPLETED"
        ]:

            icon = "🟢"

        elif notification_type in [
            "WARNING",
            "ALERT"
        ]:

            icon = "🟠"

        elif notification_type in [
            "ERROR",
            "URGENT"
        ]:

            icon = "🔴"

        else:

            icon = "🔵"


        # --------------------------------------------------
        # DISPLAY
        # --------------------------------------------------

        with st.container(
            border=True
        ):

            col1, col2 = st.columns(
                [8, 2]
            )


            with col1:

                if is_read:

                    st.markdown(
                        f"#### {icon} {title}"
                    )

                else:

                    st.markdown(
                        f"#### 🔔 {icon} {title}"
                    )


                if message:

                    st.write(
                        message
                    )


                if created_at:

                    st.caption(
                        f"🕒 {created_at}"
                    )


            with col2:

                if is_read:

                    st.caption(
                        "✓ Read"
                    )

                else:

                    st.caption(
                        "● Unread"
                    )


                    if st.button(
                        "Mark Read",
                        key=(
                            f"mark_read_"
                            f"{row_number}_"
                            f"{index}"
                        ),
                        use_container_width=True
                    ):

                        try:

                            # Expected Read column = 8
                            update_value(
                                NOTIFICATIONS,
                                row_number,
                                8,
                                "YES"
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Unable to mark as read: {e}"
                            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Notifications are displayed according to your "
    "user account / role."
)
