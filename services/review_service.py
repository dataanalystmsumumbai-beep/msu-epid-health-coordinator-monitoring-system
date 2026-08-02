from uuid import uuid4
from datetime import datetime

from config.config import DAILY_REVIEW
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class ReviewService:

    @staticmethod
    def get_all_reviews():

        try:

            data = read_all(DAILY_REVIEW)

            return data if data else []

        except Exception:

            return []

    @staticmethod
    def get_reviews_by_coordinator(coordinator_id):

        data = ReviewService.get_all_reviews()

        return [

            row

            for row in data

            if str(row.get("Coordinator_ID", "")) == str(coordinator_id)

        ]

    @staticmethod
    def get_reviews_by_date(review_date):

        data = ReviewService.get_all_reviews()

        return [

            row

            for row in data

            if str(row.get("Date", "")) == str(review_date)

        ]

    @staticmethod
    def create_review(

        review_date,
        coordinator_id,
        task_id,
        status,
        remarks=""

    ):

        review_id = "REV-" + uuid4().hex[:6].upper()

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

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

        insert_row(

            DAILY_REVIEW,
            row

        )

        return True, "Daily Review Saved Successfully."

    @staticmethod
    def update_review(

        row_no,
        status,
        remarks

    ):

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

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

        return True, "Review Updated Successfully."

    @staticmethod
    def delete_review(row_no):

        update_value(

            DAILY_REVIEW,
            row_no,
            5,
            "DELETED"

        )

        return True, "Review Deleted Successfully."

    @staticmethod
    def statistics():

        data = ReviewService.get_all_reviews()

        total = len(data)

        completed = sum(

            1

            for row in data

            if str(row.get("Status", "")).upper() == "COMPLETED"

        )

        pending = sum(

            1

            for row in data

            if str(row.get("Status", "")).upper() == "PENDING"

        )

        in_progress = sum(

            1

            for row in data

            if str(row.get("Status", "")).upper() == "IN PROGRESS"

        )

        return {

            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress

        }

    @staticmethod
    def completion_percentage():

        stats = ReviewService.statistics()

        if stats["total"] == 0:

            return 0

        return round(

            (stats["completed"] / stats["total"]) * 100,

            2

        )
