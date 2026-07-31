from datetime import datetime
from uuid import uuid4

from config.config import TASK_MASTER
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class TaskService:

    @staticmethod
    def get_all_tasks():
        try:
            return read_all(TASK_MASTER)
        except Exception:
            return []

    @staticmethod
    def create_task(
        task_name,
        category,
        frequency,
        priority,
        task_link,
        remarks=""
    ):

        task_id = "TASK-" + uuid4().hex[:6].upper()

        row = [
            task_id,
            task_name,
            category,
            frequency,
            priority,
            task_link,
            "ACTIVE",
            remarks
        ]

        insert_row(
            TASK_MASTER,
            row
        )

        return True, "Task Created Successfully"

    @staticmethod
    def statistics():

        tasks = TaskService.get_all_tasks()

        total = len(tasks)

        active = len(
            [
                t for t in tasks
                if t["Status"] == "ACTIVE"
            ]
        )

        inactive = len(
            [
                t for t in tasks
                if t["Status"] == "INACTIVE"
            ]
        )

        return {

            "total": total,

            "active": active,

            "inactive": inactive

        }
