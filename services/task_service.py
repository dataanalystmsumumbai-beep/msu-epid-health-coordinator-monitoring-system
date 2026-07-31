from datetime import datetime
from uuid import uuid4

from config.config import TASK_MASTER
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class TaskService:

    # ==========================================
    # Get All Tasks
    # ==========================================

    @staticmethod
    def get_all_tasks():

        try:
            return read_all(TASK_MASTER)

        except Exception:

            return []

    # ==========================================
    # Get Task By ID
    # ==========================================

    @staticmethod
    def get_task(task_id):

        tasks = TaskService.get_all_tasks()

        for task in tasks:

            if str(task["Task_ID"]) == str(task_id):

                return task

        return None

    # ==========================================
    # Get Coordinator Tasks
    # ==========================================

    @staticmethod
    def get_coordinator_tasks(username):

        tasks = TaskService.get_all_tasks()

        result = []

        for task in tasks:

            if str(task["Assigned_To"]).lower() == str(username).lower():

                result.append(task)

        return result

    # ==========================================
    # Create Task
    # ==========================================

    @staticmethod
    def create_task(

        task_name,
        description,
        assigned_to,
        priority,
        due_date,
        created_by

    ):

        task_id = "TASK-" + uuid4().hex[:8].upper()

        row = [

            task_id,

            task_name,

            description,

            assigned_to,

            priority,

            "Pending",

            due_date,

            datetime.now().strftime("%d-%m-%Y %H:%M"),

            created_by,

            "",

            ""

        ]

        insert_row(

            TASK_MASTER,

            row

        )

        return True, "Task Created Successfully"

    # ==========================================
    # Update Status
    # ==========================================

    @staticmethod
    def update_status(

        row_number,

        status

    ):

        try:

            update_value(

                TASK_MASTER,

                row_number,

                6,

                status

            )

            return True

        except Exception:

            return False

    # ==========================================
    # Update Remarks
    # ==========================================

    @staticmethod
    def update_remarks(

        row_number,

        remarks

    ):

        try:

            update_value(

                TASK_MASTER,

                row_number,

                10,

                remarks

            )

            return True

        except Exception:

            return False

    # ==========================================
    # Dashboard Statistics
    # ==========================================

    @staticmethod
    def statistics():

        tasks = TaskService.get_all_tasks()

        total = len(tasks)

        pending = 0

        completed = 0

        progress = 0

        for task in tasks:

            status = str(task.get("Status", "")).lower()

            if status == "pending":

                pending += 1

            elif status == "completed":

                completed += 1

        if total > 0:

            progress = round(

                completed / total * 100,

                2

            )

        return {

            "total": total,

            "pending": pending,

            "completed": completed,

            "progress": progress

        }

    # ==========================================
    # Search Tasks
    # ==========================================

    @staticmethod
    def search(keyword):

        tasks = TaskService.get_all_tasks()

        keyword = keyword.lower()

        return [

            task

            for task in tasks

            if keyword in str(task).lower()

        ]

    # ==========================================
    # Priority Filter
    # ==========================================

    @staticmethod
    def filter_priority(priority):

        tasks = TaskService.get_all_tasks()

        return [

            task

            for task in tasks

            if task["Priority"] == priority

        ]

    # ==========================================
    # Status Filter
    # ==========================================

    @staticmethod
    def filter_status(status):

        tasks = TaskService.get_all_tasks()

        return [

            task

            for task in tasks

            if task["Status"] == status

        ]
