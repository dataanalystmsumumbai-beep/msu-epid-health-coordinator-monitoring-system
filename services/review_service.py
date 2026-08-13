from uuid import uuid4
from datetime import datetime

from config.config import DAILY_REVIEW

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class ReviewService:

    # ======================================================
    # GET ALL REVIEWS
    # ======================================================

    @staticmethod
    def get_all_reviews():

        try:

            data = read_all(
                DAILY_REVIEW
            )

            return data if data else []

        except Exception:

            return []


    # ======================================================
    # ALIAS
    # ======================================================

    @staticmethod
    def get_all():

        return ReviewService.get_all_reviews()


    # ======================================================
    # GET REVIEWS BY COORDINATOR
    # ======================================================

    @staticmethod
    def get_reviews_by_coordinator(
        coordinator_id
    ):

        data = (
            ReviewService
            .get_all_reviews()
        )

        return [

            row

            for row in data

            if str(
                row.get(
                    "Coordinator_ID",
                    ""
                )
            ).strip()

            ==

            str(
                coordinator_id
            ).strip()

            and

            str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            != "DELETED"

        ]


    # ======================================================
    # GET REVIEWS BY DATE
    # ======================================================

    @staticmethod
    def get_reviews_by_date(
        review_date
    ):

        data = (
            ReviewService
            .get_all_reviews()
        )

        return [

            row

            for row in data

            if str(
                row.get(
                    "Date",
                    ""
                )
            ).strip()

            ==

            str(
                review_date
            ).strip()

            and

            str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            != "DELETED"

        ]


    # ======================================================
    # CREATE REVIEW
    # ======================================================

    @staticmethod
    def create_review(

        review_date,
        coordinator_id,
        task_id,
        status,
        remarks=""

    ):

        review_id = (
            "REV-"
            + uuid4().hex[:8].upper()
        )

        current_time = (
            datetime.now()
            .strftime(
                "%d-%m-%Y %H:%M"
            )
        )


        row = [

            review_id,

            review_date,

            coordinator_id,

            task_id,

            status,

            remarks,

            current_time,

            current_time

        ]


        try:

            insert_row(
                DAILY_REVIEW,
                row
            )

            return (
                True,
                "Daily Review Saved Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to save Daily Review: {e}"
            )


    # ======================================================
    # UPDATE REVIEW
    # ======================================================

    @staticmethod
    def update_review(

        row_no,
        status,
        remarks

    ):

        current_time = (
            datetime.now()
            .strftime(
                "%d-%m-%Y %H:%M"
            )
        )


        try:

            update_value(
                DAILY_REVIEW,
                row_no,
                5,
                status
            )


            update_value(
                DAILY_REVIEW,
                row_no,
                6,
                remarks
            )


            update_value(
                DAILY_REVIEW,
                row_no,
                8,
                current_time
            )


            return (
                True,
                "Review Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update review: {e}"
            )


    # ======================================================
    # DELETE REVIEW
    # ======================================================

    @staticmethod
    def delete_review(
        row_no
    ):

        try:

            update_value(
                DAILY_REVIEW,
                row_no,
                5,
                "DELETED"
            )

            return (
                True,
                "Review Deleted Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to delete review: {e}"
            )


    # ======================================================
    # STATISTICS
    # ======================================================

    @staticmethod
    def statistics():

        data = (
            ReviewService
            .get_all_reviews()
        )


        active_data = [

            row

            for row in data

            if str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            != "DELETED"

        ]


        total = len(
            active_data
        )


        completed = sum(

            1

            for row in active_data

            if str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            == "COMPLETED"

        )


        pending = sum(

            1

            for row in active_data

            if str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            == "PENDING"

        )


        in_progress = sum(

            1

            for row in active_data

            if str(
                row.get(
                    "Status",
                    ""
                )
            ).strip().upper()

            in [
                "IN PROGRESS",
                "IN_PROGRESS"
            ]

        )


        return {

            "total":
                total,

            "completed":
                completed,

            "pending":
                pending,

            "in_progress":
                in_progress

        }


    # ======================================================
    # COMPLETION PERCENTAGE
    # ======================================================

    @staticmethod
    def completion_percentage():

        stats = (
            ReviewService
            .statistics()
        )


        if stats["total"] == 0:

            return 0


        return round(

            (
                stats["completed"]
                /
                stats["total"]
            )
            * 100,

            2

        )
