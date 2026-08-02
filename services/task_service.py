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
            tasks = read_all(TASK_MASTER)

            return tasks if tasks else []

        except Exception:

            return []

    @staticmethod
    def get_task(task_id):

        tasks = TaskService.get_all_tasks()

        for task in tasks:

            if str(task.get("Task_ID", "")) == str(task_id):
                return task

        return None

    @staticmethod
    def create_task(
        task_name,
        category,
        frequency,
        priority,
        task_link="",
        remarks=""
    ):

        task_name = task_name.strip()

        if task_name == "":
            return False, "Task Name is required."

        tasks = TaskService.get_all_tasks()

        for task in tasks:

            if str(task.get("Task_Name", "")).strip().lower() == task_name.lower():

                return False, "Task already exists."

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

        return True, "Task Created Successfully."

    @staticmethod
    def activate_task(row_no):

        update_value(
            TASK_MASTER,
            row_no,
            7,
            "ACTIVE"
        )

        return True, "Task Activated."

    @staticmethod
    def deactivate_task(row_no):

        update_value(
            TASK_MASTER,
            row_no,
            7,
            "INACTIVE"
        )

        return True, "Task Deactivated."

    @staticmethod
    def update_task(
        row_no,
        task_name,
        category,
        frequency,
        priority,
        task_link,
        remarks
    ):

        update_value(TASK_MASTER, row_no, 2, task_name)
        update_value(TASK_MASTER, row_no, 3, category)
        update_value(TASK_MASTER, row_no, 4, frequency)
        update_value(TASK_MASTER, row_no, 5, priority)
        update_value(TASK_MASTER, row_no, 6, task_link)
        update_value(TASK_MASTER, row_no, 8, remarks)

        return True, "Task Updated Successfully."

    @staticmethod
    def statistics():

        tasks = TaskService.get_all_tasks()

        total = len(tasks)

        active = sum(
            1
            for t in tasks
            if str(t.get("Status", "")) == "ACTIVE"
        )

        inactive = sum(
            1
            for t in tasks
            if str(t.get("Status", "")) == "INACTIVE"
        )

        return {

            "total": total,
            "active": active,
            "inactive": inactive

        }
