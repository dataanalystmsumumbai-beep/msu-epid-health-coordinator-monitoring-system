from uuid import uuid4

from config.config import COORDINATOR_TASK_MAP

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class TaskAssignmentService:

    @staticmethod
    def get_all_assignments():

        try:

            data = read_all(COORDINATOR_TASK_MAP)

            return data if data else []

        except Exception:

            return []

    @staticmethod
    def assign_task(

        coordinator_id,
        task_id,
        assigned_by,
        assigned_date,
        due_date,
        priority,
        remarks=""

    ):

        assignment_id = "ASN-" + uuid4().hex[:6].upper()

        row = [

            assignment_id,
            coordinator_id,
            task_id,
            assigned_by,
            assigned_date,
            due_date,
            priority,
            "Pending",
            remarks

        ]

        insert_row(
            COORDINATOR_TASK_MAP,
            row
        )

        return True, "Task Assigned Successfully."

    @staticmethod
    def coordinator_tasks(coordinator_id):

        assignments = TaskAssignmentService.get_all_assignments()

        return [

            x

            for x in assignments

            if str(
                x.get("Coordinator_ID", "")
            ) == str(coordinator_id)

        ]

    @staticmethod
    def update_status(

        row_no,
        status

    ):

        update_value(
            COORDINATOR_TASK_MAP,
            row_no,
            8,
            status
        )

        return True
