from uuid import uuid4

from config.config import COORDINATOR_TASK_MAP

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class TaskAssignmentService:

    # ======================================================
    # GET ALL ASSIGNMENTS
    # ======================================================

    @staticmethod
    def get_all_assignments():

        try:

            data = read_all(
                COORDINATOR_TASK_MAP
            )

            return data if data else []

        except Exception:

            return []


    # ======================================================
    # ASSIGN TASK
    # ======================================================

    @staticmethod
    def assign_task(
        coordinator_id,
        task_id,
        assigned_by,
        assigned_date="",
        due_date="",
        priority="Medium",
        remarks=""
    ):

        assignments = (
            TaskAssignmentService
            .get_all_assignments()
        )

        # --------------------------------------------------
        # Prevent duplicate active assignment
        # --------------------------------------------------

        for assignment in assignments:

            existing_coordinator = str(
                assignment.get(
                    "Coordinator_ID",
                    ""
                )
            ).strip()

            existing_task = str(
                assignment.get(
                    "Task_ID",
                    ""
                )
            ).strip()

            existing_status = str(
                assignment.get(
                    "Status",
                    ""
                )
            ).strip().lower()

            if (
                existing_coordinator
                == str(coordinator_id).strip()
                and
                existing_task
                == str(task_id).strip()
                and
                existing_status
                not in [
                    "removed",
                    "inactive",
                    "deleted"
                ]
            ):

                return (
                    False,
                    "This task is already assigned "
                    "to this coordinator."
                )

        # --------------------------------------------------
        # Assignment ID
        # --------------------------------------------------

        assignment_id = (
            "ASN-"
            + uuid4().hex[:8].upper()
        )

        # --------------------------------------------------
        # Google Sheet Row
        # --------------------------------------------------

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

        try:

            insert_row(
                COORDINATOR_TASK_MAP,
                row
            )

            return (
                True,
                "Task Assigned Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to assign task: {e}"
            )


    # ======================================================
    # GET COORDINATOR TASKS
    # ======================================================

    @staticmethod
    def coordinator_tasks(
        coordinator_id
    ):

        assignments = (
            TaskAssignmentService
            .get_all_assignments()
        )

        return [

            assignment

            for assignment in assignments

            if str(
                assignment.get(
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
                assignment.get(
                    "Status",
                    ""
                )
            ).strip().lower()

            not in [
                "removed",
                "inactive",
                "deleted"
            ]

        ]


    # ======================================================
    # ALIAS — USED BY TASK MANAGEMENT PAGE
    # ======================================================

    @staticmethod
    def get_coordinator_tasks(
        coordinator_id
    ):

        return (
            TaskAssignmentService
            .coordinator_tasks(
                coordinator_id
            )
        )


    # ======================================================
    # REMOVE ASSIGNMENT
    # ======================================================

    @staticmethod
    def remove_assignment(
        coordinator_id,
        task_id,
        modified_by="SYSTEM"
    ):

        assignments = (
            TaskAssignmentService
            .get_all_assignments()
        )

        for index, assignment in enumerate(
            assignments,
            start=2
        ):

            existing_coordinator = str(
                assignment.get(
                    "Coordinator_ID",
                    ""
                )
            ).strip()

            existing_task = str(
                assignment.get(
                    "Task_ID",
                    ""
                )
            ).strip()

            existing_status = str(
                assignment.get(
                    "Status",
                    ""
                )
            ).strip().lower()

            if (
                existing_coordinator
                == str(coordinator_id).strip()

                and

                existing_task
                == str(task_id).strip()

                and

                existing_status
                not in [
                    "removed",
                    "inactive",
                    "deleted"
                ]
            ):

                try:

                    # Status column = 8
                    update_value(
                        COORDINATOR_TASK_MAP,
                        index,
                        8,
                        "Removed"
                    )

                    return (
                        True,
                        "Task assignment removed successfully."
                    )

                except Exception as e:

                    return (
                        False,
                        f"Unable to remove assignment: {e}"
                    )

        return (
            False,
            "Assignment not found."
        )


    # ======================================================
    # UPDATE STATUS
    # ======================================================

    @staticmethod
    def update_status(
        row_no,
        status
    ):

        try:

            update_value(
                COORDINATOR_TASK_MAP,
                row_no,
                8,
                status
            )

            return (
                True,
                "Task status updated successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update task status: {e}"
            )


    # ======================================================
    # UPDATE ASSIGNMENT
    # ======================================================

    @staticmethod
    def update_assignment(
        row_no,
        due_date=None,
        priority=None,
        status=None,
        remarks=None
    ):

        try:

            # Column 6 = Due Date
            if due_date is not None:

                update_value(
                    COORDINATOR_TASK_MAP,
                    row_no,
                    6,
                    due_date
                )

            # Column 7 = Priority
            if priority is not None:

                update_value(
                    COORDINATOR_TASK_MAP,
                    row_no,
                    7,
                    priority
                )

            # Column 8 = Status
            if status is not None:

                update_value(
                    COORDINATOR_TASK_MAP,
                    row_no,
                    8,
                    status
                )

            # Column 9 = Remarks
            if remarks is not None:

                update_value(
                    COORDINATOR_TASK_MAP,
                    row_no,
                    9,
                    remarks
                )

            return (
                True,
                "Assignment updated successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update assignment: {e}"
            )
