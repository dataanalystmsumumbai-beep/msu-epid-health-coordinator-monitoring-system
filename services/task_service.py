from uuid import uuid4

from config.config import TASK_MASTER

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class TaskService:

    # ======================================================
    # GET ALL TASKS
    # ======================================================

    @staticmethod
    def get_all_tasks():

        try:

            data = read_all(
                TASK_MASTER
            )

            return data if data else []

        except Exception:

            return []


    # ======================================================
    # GET TASK
    # ======================================================

    @staticmethod
    def get_task(task_id):

        task_id = str(
            task_id or ""
        ).strip()


        for task in TaskService.get_all_tasks():

            current_id = str(
                task.get(
                    "Task_ID",
                    ""
                )
            ).strip()


            if current_id == task_id:

                return task


        return None


    # ======================================================
    # CREATE TASK
    # ======================================================

    @staticmethod
    def create_task(
        task_name,
        category,
        frequency,
        priority,
        task_link="",
        remarks=""
    ):

        task_name = str(
            task_name or ""
        ).strip()


        if not task_name:

            return (
                False,
                "Task Name is required."
            )


        existing_tasks = (
            TaskService
            .get_all_tasks()
        )


        for task in existing_tasks:

            existing_name = str(
                task.get(
                    "Task_Name",
                    ""
                )
            ).strip().lower()


            existing_status = str(
                task.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()


            if (
                existing_name
                == task_name.lower()
                and existing_status != "DELETED"
            ):

                return (
                    False,
                    "Task already exists."
                )


        task_id = (
            "TASK-"
            + uuid4().hex[:6].upper()
        )


        row = [

            task_id,

            task_name,

            str(
                category or ""
            ).strip(),

            str(
                frequency or ""
            ).strip(),

            str(
                priority or ""
            ).strip(),

            str(
                task_link or ""
            ).strip(),

            "ACTIVE",

            str(
                remarks or ""
            ).strip()

        ]


        try:

            insert_row(
                TASK_MASTER,
                row
            )

            return (
                True,
                "Task Created Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to create task: {e}"
            )


    # ======================================================
    # UPDATE TASK
    # ======================================================

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

        if not row_no:

            return (
                False,
                "Invalid task row."
            )


        task_name = str(
            task_name or ""
        ).strip()


        if not task_name:

            return (
                False,
                "Task Name is required."
            )


        try:

            update_value(
                TASK_MASTER,
                row_no,
                2,
                task_name
            )

            update_value(
                TASK_MASTER,
                row_no,
                3,
                str(
                    category or ""
                ).strip()
            )

            update_value(
                TASK_MASTER,
                row_no,
                4,
                str(
                    frequency or ""
                ).strip()
            )

            update_value(
                TASK_MASTER,
                row_no,
                5,
                str(
                    priority or ""
                ).strip()
            )

            update_value(
                TASK_MASTER,
                row_no,
                6,
                str(
                    task_link or ""
                ).strip()
            )

            update_value(
                TASK_MASTER,
                row_no,
                8,
                str(
                    remarks or ""
                ).strip()
            )


            return (
                True,
                "Task Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update task: {e}"
            )


    # ======================================================
    # ACTIVATE TASK
    # ======================================================

    @staticmethod
    def activate_task(
        row_no
    ):

        try:

            update_value(
                TASK_MASTER,
                row_no,
                7,
                "ACTIVE"
            )

            return (
                True,
                "Task Activated."
            )

        except Exception as e:

            return (
                False,
                f"Unable to activate task: {e}"
            )


    # ======================================================
    # DEACTIVATE TASK
    # ======================================================

    @staticmethod
    def deactivate_task(
        row_no
    ):

        try:

            update_value(
                TASK_MASTER,
                row_no,
                7,
                "INACTIVE"
            )

            return (
                True,
                "Task Deactivated."
            )

        except Exception as e:

            return (
                False,
                f"Unable to deactivate task: {e}"
            )


    # ======================================================
    # DELETE TASK
    # ======================================================

    @staticmethod
    def delete_task(
        row_no
    ):

        try:

            update_value(
                TASK_MASTER,
                row_no,
                7,
                "DELETED"
            )

            return (
                True,
                "Task Archived Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to archive task: {e}"
            )


    # ======================================================
    # ACTIVE TASKS
    # ======================================================

    @staticmethod
    def get_active_tasks():

        return [

            task

            for task in (
                TaskService
                .get_all_tasks()
            )

            if str(
                task.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "ACTIVE"

        ]


    # ======================================================
    # STATISTICS
    # ======================================================

    @staticmethod
    def statistics():

        tasks = (
            TaskService
            .get_all_tasks()
        )


        active = sum(

            1

            for task in tasks

            if str(
                task.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "ACTIVE"

        )


        inactive = sum(

            1

            for task in tasks

            if str(
                task.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "INACTIVE"

        )


        deleted = sum(

            1

            for task in tasks

            if str(
                task.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "DELETED"

        )


        return {

            "total":
                len(tasks),

            "active":
                active,

            "inactive":
                inactive,

            "deleted":
                deleted

        }


    # ======================================================
    # TOTAL TASKS
    # ======================================================

    @staticmethod
    def total_tasks():

        return len(
            TaskService
            .get_active_tasks()
        )
