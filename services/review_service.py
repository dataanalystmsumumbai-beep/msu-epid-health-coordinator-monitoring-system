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

        return (
            ReviewService
            .get_all_reviews()
        )


    # ======================================================
    # NORMALIZE
    # ======================================================

    @staticmethod
    def _normalize(value):

        return str(
            value
            if value is not None
            else ""
        ).strip()


    # ======================================================
    # GET REVIEWS BY COORDINATOR
    # ======================================================

    @staticmethod
    def get_reviews_by_coordinator(
        coordinator_id
    ):

        coordinator_id = (
            ReviewService
            ._normalize(
                coordinator_id
            )
        )

        data = (
            ReviewService
            .get_all_reviews()
        )

        return [

            row

            for row in data

            if ReviewService._normalize(
                row.get(
                    "Coordinator_ID",
                    ""
                )
            )
            == coordinator_id

            and ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()
            != "DELETED"

        ]


    # ======================================================
    # GET REVIEWS BY DATE
    # ======================================================

    @staticmethod
    def get_reviews_by_date(
        review_date
    ):

        review_date = (
            ReviewService
            ._normalize(
                review_date
            )
        )

        data = (
            ReviewService
            .get_all_reviews()
        )

        return [

            row

            for row in data

            if ReviewService._normalize(
                row.get(
                    "Date",
                    row.get(
                        "Review_Date",
                        ""
                    )
                )
            )
            == review_date

            and ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()
            != "DELETED"

        ]


    # ======================================================
    # GET REVIEWS BY DATE RANGE
    # ======================================================

    @staticmethod
    def get_reviews_by_date_range(
        start_date,
        end_date
    ):

        try:

            start = datetime.strptime(
                str(start_date),
                "%d-%m-%Y"
            ).date()

            end = datetime.strptime(
                str(end_date),
                "%d-%m-%Y"
            ).date()

        except Exception:

            return []


        data = (
            ReviewService
            .get_all_reviews()
        )

        results = []


        for row in data:

            status = (
                ReviewService
                ._normalize(
                    row.get(
                        "Status",
                        ""
                    )
                )
                .upper()
            )

            if status == "DELETED":

                continue


            date_text = (
                ReviewService
                ._normalize(
                    row.get(
                        "Date",
                        row.get(
                            "Review_Date",
                            ""
                        )
                    )
                )
            )


            try:

                current_date = (
                    datetime.strptime(
                        date_text,
                        "%d-%m-%Y"
                    ).date()
                )

            except Exception:

                continue


            if (
                start
                <= current_date
                <= end
            ):

                results.append(
                    row
                )


        return results


    # ======================================================
    # CHECK DAILY SUBMISSION
    # ======================================================

    @staticmethod
    def is_submitted(
        coordinator_id,
        task_id,
        review_date
    ):

        coordinator_id = (
            ReviewService
            ._normalize(
                coordinator_id
            )
        )

        task_id = (
            ReviewService
            ._normalize(
                task_id
            )
        )

        review_date = (
            ReviewService
            ._normalize(
                review_date
            )
        )


        reviews = (
            ReviewService
            .get_all_reviews()
        )


        for review in reviews:

            existing_coordinator = (
                ReviewService
                ._normalize(
                    review.get(
                        "Coordinator_ID",
                        ""
                    )
                )
            )

            existing_task = (
                ReviewService
                ._normalize(
                    review.get(
                        "Task_ID",
                        ""
                    )
                )
            )

            existing_date = (
                ReviewService
                ._normalize(
                    review.get(
                        "Date",
                        review.get(
                            "Review_Date",
                            ""
                        )
                    )
                )
            )

            existing_status = (
                ReviewService
                ._normalize(
                    review.get(
                        "Status",
                        ""
                    )
                )
                .upper()
            )


            if (

                existing_coordinator
                == coordinator_id

                and

                existing_task
                == task_id

                and

                existing_date
                == review_date

                and

                existing_status
                != "DELETED"

            ):

                return True


        return False


    # ======================================================
    # GET EXISTING SUBMISSION
    # ======================================================

    @staticmethod
    def get_submission(
        coordinator_id,
        task_id,
        review_date
    ):

        coordinator_id = (
            ReviewService
            ._normalize(
                coordinator_id
            )
        )

        task_id = (
            ReviewService
            ._normalize(
                task_id
            )
        )

        review_date = (
            ReviewService
            ._normalize(
                review_date
            )
        )


        for review in (
            ReviewService
            .get_all_reviews()
        ):

            if (

                ReviewService._normalize(
                    review.get(
                        "Coordinator_ID",
                        ""
                    )
                )
                == coordinator_id

                and

                ReviewService._normalize(
                    review.get(
                        "Task_ID",
                        ""
                    )
                )
                == task_id

                and

                ReviewService._normalize(
                    review.get(
                        "Date",
                        review.get(
                            "Review_Date",
                            ""
                        )
                    )
                )
                == review_date

                and

                ReviewService._normalize(
                    review.get(
                        "Status",
                        ""
                    )
                ).upper()
                != "DELETED"

            ):

                return review


        return None


    # ======================================================
    # CREATE REVIEW
    # ======================================================

    @staticmethod
    def create_review(
        review_date,
        coordinator_id,
        task_id,
        status,
        remarks="",
        assignment_id=""
    ):

        review_date = (
            ReviewService
            ._normalize(
                review_date
            )
        )

        coordinator_id = (
            ReviewService
            ._normalize(
                coordinator_id
            )
        )

        task_id = (
            ReviewService
            ._normalize(
                task_id
            )
        )

        status = (
            ReviewService
            ._normalize(
                status
            )
        )

        remarks = (
            ReviewService
            ._normalize(
                remarks
            )
        )


        if not review_date:

            return (
                False,
                "Review date is required."
            )


        if not coordinator_id:

            return (
                False,
                "Coordinator ID is required."
            )


        if not task_id:

            return (
                False,
                "Task ID is required."
            )


        # --------------------------------------------------
        # DATE-WISE DUPLICATE PROTECTION
        # --------------------------------------------------

        if ReviewService.is_submitted(
            coordinator_id,
            task_id,
            review_date
        ):

            return (
                False,
                (
                    "Daily Review for this task "
                    f"has already been submitted "
                    f"for {review_date}."
                )
            )


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

            assignment_id,

            status,

            remarks,

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
                6,
                status
            )


            update_value(
                DAILY_REVIEW,
                row_no,
                7,
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
                6,
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

            if ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()
            != "DELETED"

        ]


        total = len(
            active_data
        )


        completed = sum(

            1

            for row in active_data

            if ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()
            == "COMPLETED"

        )


        pending = sum(

            1

            for row in active_data

            if ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()
            == "PENDING"

        )


        in_progress = sum(

            1

            for row in active_data

            if ReviewService._normalize(
                row.get(
                    "Status",
                    ""
                )
            ).upper()

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
