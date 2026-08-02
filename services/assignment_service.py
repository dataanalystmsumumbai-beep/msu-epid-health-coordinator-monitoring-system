from uuid import uuid4

from config.config import TASK_ASSIGNMENT
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class AssignmentService:

    @staticmethod
    def get_all_assignments():

        try:
            data = read_all(TASK_ASSIGNMENT)

            return data if data else []

        except Exception:

            return []

    @staticmethod
    def get_assignment(coordinator_id):

        data = AssignmentService.get_all_assignments()

        return [

            row

            for row in data

            if str(row.get("Coordinator_ID", "")) == str(coordinator_id)

        ]

    @staticmethod
    def assign_task(

        coordinator_id,
        task_id,
        assigned_date,
        due_date,
        assigned_by,
        remarks=""

    ):

        assignment_id = "ASN-" + uuid4().hex[:6].upper()

        row = [

            assignment_id,
            coordinator_id,
            task_id,
            assigned_date,
            due_date,
            "ACTIVE",
            assigned_by,
            remarks

        ]

        insert_row(

            TASK_ASSIGNMENT,
            row

        )

        return True, "Task Assigned Successfully."

    @staticmethod
    def update_assignment(

        row_no,
        due_date,
        remarks

    ):

        update_value(

            TASK_ASSIGNMENT,
            row_no,
            5,
            due_date

        )

        update_value(

            TASK_ASSIGNMENT,
            row_no,
            8,
            remarks

        )

        return True, "Assignment Updated Successfully."

    @staticmethod
    def deactivate_assignment(row_no):

        update_value(

            TASK_ASSIGNMENT,
            row_no,
            6,
            "INACTIVE"

        )

        return True, "Assignment Closed."

    @staticmethod
    def statistics():

        data = AssignmentService.get_all_assignments()

        total = len(data)

        active = sum(

            1

            for row in data

            if str(row.get("Status", "")) == "ACTIVE"

        )

        inactive = sum(

            1

            for row in data

            if str(row.get("Status", "")) == "INACTIVE"

        )

        return {

            "total": total,
            "active": active,
            "inactive": inactive

        }
