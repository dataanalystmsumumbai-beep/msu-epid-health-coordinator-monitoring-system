from uuid import uuid4
from datetime import datetime

from config.config import NOTIFICATIONS

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class NotificationService:

    @staticmethod
    def get_all_notifications():

        try:

            data = read_all(
                NOTIFICATIONS
            )

            return data if data else []

        except Exception:

            return []


    @staticmethod
    def create_notification(
        recipient_id,
        title,
        message,
        notification_type="INFO"
    ):

        notification_id = (
            "NOT-"
            + uuid4().hex[:8].upper()
        )

        created_at = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        row = [

            notification_id,

            str(
                recipient_id or ""
            ).strip(),

            str(
                title or ""
            ).strip(),

            str(
                message or ""
            ).strip(),

            str(
                notification_type or "INFO"
            ).strip(),

            "UNREAD",

            created_at

        ]

        try:

            insert_row(
                NOTIFICATIONS,
                row
            )

            return (
                True,
                "Notification Created Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to create notification: {e}"
            )


    @staticmethod
    def get_user_notifications(
        recipient_id
    ):

        recipient_id = str(
            recipient_id or ""
        ).strip()


        return [

            notification

            for notification in (
                NotificationService
                .get_all_notifications()
            )

            if str(
                notification.get(
                    "Recipient_ID",
                    ""
                )
            ).strip()
            == recipient_id

        ]


    @staticmethod
    def get_unread_notifications(
        recipient_id
    ):

        notifications = (
            NotificationService
            .get_user_notifications(
                recipient_id
            )
        )


        return [

            notification

            for notification in notifications

            if str(
                notification.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "UNREAD"

        ]


    @staticmethod
    def unread_count(
        recipient_id
    ):

        return len(
            NotificationService
            .get_unread_notifications(
                recipient_id
            )
        )


    @staticmethod
    def mark_as_read(
        row_no
    ):

        try:

            update_value(
                NOTIFICATIONS,
                row_no,
                6,
                "READ"
            )

            return (
                True,
                "Notification marked as read."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update notification: {e}"
            )


    @staticmethod
    def mark_all_as_read(
        recipient_id
    ):

        notifications = (
            NotificationService
            .get_user_notifications(
                recipient_id
            )
        )


        updated = 0


        for index, notification in enumerate(
            notifications,
            start=2
        ):

            if str(
                notification.get(
                    "Status",
                    ""
                )
            ).strip().upper() == "UNREAD":

                try:

                    update_value(
                        NOTIFICATIONS,
                        index,
                        6,
                        "READ"
                    )

                    updated += 1

                except Exception:

                    pass


        return (
            True,
            f"{updated} notification(s) marked as read."
        )
