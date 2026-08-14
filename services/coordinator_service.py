from uuid import uuid4

from config.config import COORDINATOR_MASTER

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class CoordinatorService:

    # ======================================================
    # GET ALL COORDINATORS
    # ======================================================

    @staticmethod
    def get_all_coordinators():

        try:

            data = read_all(
                COORDINATOR_MASTER
            )

            return data if data else []

        except Exception:

            return []


    # ======================================================
    # GET COORDINATOR BY ID
    # ======================================================

    @staticmethod
    def get_coordinator(
        coordinator_id
    ):

        coordinator_id = str(
            coordinator_id or ""
        ).strip()


        if not coordinator_id:
            return None


        for coordinator in (
            CoordinatorService
            .get_all_coordinators()
        ):

            current_id = str(
                coordinator.get(
                    "Coordinator_ID",
                    ""
                )
            ).strip()


            if current_id == coordinator_id:

                return coordinator


        return None


    # ======================================================
    # CREATE COORDINATOR
    # ======================================================

    @staticmethod
    def create_coordinator(
        coordinator_name,
        user_id="",
        ward_no="",
        mobile="",
        email="",
        designation="",
        remarks=""
    ):

        coordinator_name = str(
            coordinator_name or ""
        ).strip()


        if not coordinator_name:

            return (
                False,
                "Coordinator Name is required."
            )


        existing = (
            CoordinatorService
            .get_all_coordinators()
        )


        for coordinator in existing:

            existing_name = str(
                coordinator.get(
                    "Coordinator_Name",
                    ""
                )
            ).strip().lower()


            existing_status = str(
                coordinator.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()


            if (
                existing_name
                == coordinator_name.lower()
                and existing_status != "DELETED"
            ):

                return (
                    False,
                    "Coordinator already exists."
                )


        coordinator_id = (
            "COORD-"
            + uuid4().hex[:6].upper()
        )


        row = [

            coordinator_id,

            str(
                user_id or ""
            ).strip(),

            coordinator_name,

            str(
                ward_no or ""
            ).strip(),

            str(
                mobile or ""
            ).strip(),

            str(
                email or ""
            ).strip(),

            str(
                designation or ""
            ).strip(),

            "ACTIVE",

            str(
                remarks or ""
            ).strip()

        ]


        try:

            insert_row(
                COORDINATOR_MASTER,
                row
            )

            return (
                True,
                "Coordinator Created Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to create Coordinator: {e}"
            )


    # ======================================================
    # UPDATE COORDINATOR
    # ======================================================

    @staticmethod
    def update_coordinator(
        row_no,
        coordinator_name,
        user_id,
        ward_no,
        mobile,
        email,
        designation,
        remarks
    ):

        if not row_no:

            return (
                False,
                "Invalid Coordinator row."
            )


        coordinator_name = str(
            coordinator_name or ""
        ).strip()


        if not coordinator_name:

            return (
                False,
                "Coordinator Name is required."
            )


        try:

            update_value(
                COORDINATOR_MASTER,
                row_no,
                2,
                str(
                    user_id or ""
                ).strip()
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                3,
                coordinator_name
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                4,
                str(
                    ward_no or ""
                ).strip()
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                5,
                str(
                    mobile or ""
                ).strip()
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                6,
                str(
                    email or ""
                ).strip()
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                7,
                str(
                    designation or ""
                ).strip()
            )

            update_value(
                COORDINATOR_MASTER,
                row_no,
                9,
                str(
                    remarks or ""
                ).strip()
            )


            return (
                True,
                "Coordinator Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update Coordinator: {e}"
            )


    # ======================================================
    # ACTIVATE
    # ======================================================

    @staticmethod
    def activate_coordinator(
        row_no
    ):

        try:

            update_value(
                COORDINATOR_MASTER,
                row_no,
                8,
                "ACTIVE"
            )

            return (
                True,
                "Coordinator Activated."
            )

        except Exception as e:

            return (
                False,
                f"Unable to activate Coordinator: {e}"
            )


    # ======================================================
    # DEACTIVATE
    # ======================================================

    @staticmethod
    def deactivate_coordinator(
        row_no
    ):

        try:

            update_value(
                COORDINATOR_MASTER,
                row_no,
                8,
                "INACTIVE"
            )

            return (
                True,
                "Coordinator Deactivated."
            )

        except Exception as e:

            return (
                False,
                f"Unable to deactivate Coordinator: {e}"
            )


    # ======================================================
    # DELETE
    # ======================================================

    @staticmethod
    def delete_coordinator(
        row_no
    ):

        try:

            update_value(
                COORDINATOR_MASTER,
                row_no,
                8,
                "DELETED"
            )

            return (
                True,
                "Coordinator Archived Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to archive Coordinator: {e}"
            )


    # ======================================================
    # ACTIVE COORDINATORS
    # ======================================================

    @staticmethod
    def get_active_coordinators():

        return [

            coordinator

            for coordinator in (
                CoordinatorService
                .get_all_coordinators()
            )

            if str(
                coordinator.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "ACTIVE"

        ]


    # ======================================================
    # COORDINATORS BY WARD
    # ======================================================

    @staticmethod
    def get_by_ward(
        ward_no
    ):

        ward_no = str(
            ward_no or ""
        ).strip()


        return [

            coordinator

            for coordinator in (
                CoordinatorService
                .get_active_coordinators()
            )

            if str(
                coordinator.get(
                    "Ward_No",
                    ""
                )
            ).strip()
            == ward_no

        ]


    # ======================================================
    # STATISTICS
    # ======================================================

    @staticmethod
    def statistics():

        coordinators = (
            CoordinatorService
            .get_all_coordinators()
        )


        active = sum(

            1

            for coordinator in coordinators

            if str(
                coordinator.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "ACTIVE"

        )


        inactive = sum(

            1

            for coordinator in coordinators

            if str(
                coordinator.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "INACTIVE"

        )


        deleted = sum(

            1

            for coordinator in coordinators

            if str(
                coordinator.get(
                    "Status",
                    ""
                )
            ).strip().upper()
            == "DELETED"

        )


        return {

            "total":
                len(coordinators),

            "active":
                active,

            "inactive":
                inactive,

            "deleted":
                deleted

        }


    # ======================================================
    # TOTAL ACTIVE
    # ======================================================

    @staticmethod
    def total_coordinators():

        return len(
            CoordinatorService
            .get_active_coordinators()
        )
