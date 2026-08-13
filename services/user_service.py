from datetime import datetime
import hashlib

from config.config import (
    USER_MASTER,
    ROLE_DEVELOPER,
    ROLE_ADMIN,
    ROLE_COORDINATOR
)

from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class UserService:

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def _now():

        return datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )


    @staticmethod
    def _hash_password(password):

        return hashlib.sha256(
            str(password)
            .encode("utf-8")
        ).hexdigest()


    @staticmethod
    def _role(value):

        return str(
            value or ""
        ).strip().lower()


    @staticmethod
    def _row_number(user):

        for key in [
            "_row",
            "Row",
            "row",
            "Row_Number",
            "row_number"
        ]:

            if key in user:

                try:
                    return int(
                        user[key]
                    )
                except Exception:
                    pass

        return None


    # ======================================================
    # GET ALL USERS
    # ======================================================

    @staticmethod
    def get_all_users():

        try:

            return (
                read_all(
                    USER_MASTER
                )
                or []
            )

        except Exception:

            return []


    # ======================================================
    # GET USER
    # ======================================================

    @staticmethod
    def get_user(username):

        if not username:
            return None

        username = str(
            username
        ).strip().lower()


        for user in UserService.get_all_users():

            db_username = str(
                user.get(
                    "Username",
                    ""
                )
            ).strip().lower()


            if db_username == username:

                return user


        return None


    # ======================================================
    # GET USER BY ID
    # ======================================================

    @staticmethod
    def get_user_by_id(user_id):

        if not user_id:
            return None

        user_id = str(
            user_id
        ).strip()


        for user in UserService.get_all_users():

            db_id = str(
                user.get(
                    "User_ID",
                    ""
                )
            ).strip()


            if db_id == user_id:

                return user


        return None


    # ======================================================
    # USERNAME EXISTS
    # ======================================================

    @staticmethod
    def username_exists(username):

        return (
            UserService
            .get_user(username)
            is not None
        )


    # ======================================================
    # GENERATE USER ID
    # ======================================================

    @staticmethod
    def generate_user_id():

        users = (
            UserService
            .get_all_users()
        )

        max_id = 0


        for user in users:

            uid = str(
                user.get(
                    "User_ID",
                    ""
                )
            ).strip().upper()


            if uid.startswith("USR"):

                try:

                    number = int(
                        uid.replace(
                            "USR",
                            ""
                        )
                    )

                    max_id = max(
                        max_id,
                        number
                    )

                except Exception:
                    pass


        return (
            f"USR{max_id + 1:03d}"
        )


    # ======================================================
    # CREATE USER
    # ======================================================

    @staticmethod
    def create_user(
        username,
        password,
        role,
        full_name,
        designation="",
        mobile="",
        email="",
        created_by="SYSTEM"
    ):

        username = str(
            username or ""
        ).strip()

        password = str(
            password or ""
        ).strip()

        role = str(
            role or ""
        ).strip()

        full_name = str(
            full_name or ""
        ).strip()

        designation = str(
            designation or ""
        ).strip()

        mobile = str(
            mobile or ""
        ).strip()

        email = str(
            email or ""
        ).strip()


        if not username:

            return (
                False,
                "Username is required."
            )


        if not password:

            return (
                False,
                "Password is required."
            )


        if not full_name:

            return (
                False,
                "Full Name is required."
            )


        if role not in [
            ROLE_DEVELOPER,
            ROLE_ADMIN,
            ROLE_COORDINATOR
        ]:

            return (
                False,
                "Invalid user role."
            )


        if UserService.username_exists(
            username
        ):

            return (
                False,
                "Username already exists."
            )


        password_hash = (
            UserService
            ._hash_password(
                password
            )
        )


        current_time = (
            UserService
            ._now()
        )


        row = [

            UserService.generate_user_id(),

            username,

            password_hash,

            role,

            full_name,

            designation,

            mobile,

            email,

            "ACTIVE",

            "",

            current_time,

            0,

            "NO",

            current_time,

            created_by,

            "",

            "",

            ""

        ]


        try:

            insert_row(
                USER_MASTER,
                row
            )

            return (
                True,
                "User Created Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to create user: {e}"
            )


    # ======================================================
    # UPDATE USER DETAILS
    # ======================================================

    @staticmethod
    def update_user(
        row_no,
        full_name,
        designation,
        mobile,
        email,
        role,
        modified_by="SYSTEM"
    ):

        if not row_no:

            return (
                False,
                "Invalid user row."
            )


        role = str(
            role or ""
        ).strip()


        if role not in [
            ROLE_DEVELOPER,
            ROLE_ADMIN,
            ROLE_COORDINATOR
        ]:

            return (
                False,
                "Invalid user role."
            )


        current_time = (
            UserService
            ._now()
        )


        try:

            update_value(
                USER_MASTER,
                row_no,
                4,
                role
            )

            update_value(
                USER_MASTER,
                row_no,
                5,
                str(
                    full_name or ""
                ).strip()
            )

            update_value(
                USER_MASTER,
                row_no,
                6,
                str(
                    designation or ""
                ).strip()
            )

            update_value(
                USER_MASTER,
                row_no,
                7,
                str(
                    mobile or ""
                ).strip()
            )

            update_value(
                USER_MASTER,
                row_no,
                8,
                str(
                    email or ""
                ).strip()
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )


            return (
                True,
                "User Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update user: {e}"
            )


    # ======================================================
    # CHANGE PASSWORD
    # ======================================================

    @staticmethod
    def change_password(
        row_no,
        new_password,
        modified_by="SYSTEM"
    ):

        new_password = str(
            new_password or ""
        ).strip()


        if not row_no:

            return (
                False,
                "Invalid user row."
            )


        if not new_password:

            return (
                False,
                "New password is required."
            )


        if len(new_password) < 8:

            return (
                False,
                "Password must contain at least 8 characters."
            )


        password_hash = (
            UserService
            ._hash_password(
                new_password
            )
        )


        current_time = (
            UserService
            ._now()
        )


        try:

            update_value(
                USER_MASTER,
                row_no,
                3,
                password_hash
            )

            update_value(
                USER_MASTER,
                row_no,
                11,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                12,
                0
            )

            update_value(
                USER_MASTER,
                row_no,
                13,
                "NO"
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )


            return (
                True,
                "Password Changed Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to change password: {e}"
            )


    # ======================================================
    # RESET PASSWORD
    # ======================================================

    @staticmethod
    def reset_password(
        row_no,
        new_password,
        modified_by="SYSTEM"
    ):

        return UserService.change_password(
            row_no,
            new_password,
            modified_by
        )


    # ======================================================
    # LOCK USER
    # ======================================================

    @staticmethod
    def lock_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = (
            UserService
            ._now()
        )

        try:

            update_value(
                USER_MASTER,
                row_no,
                13,
                "YES"
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "User Locked Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to lock user: {e}"
            )


    # ======================================================
    # UNLOCK USER
    # ======================================================

    @staticmethod
    def unlock_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = (
            UserService
            ._now()
        )

        try:

            update_value(
                USER_MASTER,
                row_no,
                13,
                "NO"
            )

            update_value(
                USER_MASTER,
                row_no,
                12,
                0
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "User Unlocked Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to unlock user: {e}"
            )


    # ======================================================
    # ENABLE USER
    # ======================================================

    @staticmethod
    def enable_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = (
            UserService
            ._now()
        )

        try:

            update_value(
                USER_MASTER,
                row_no,
                9,
                "ACTIVE"
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "User Enabled Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to enable user: {e}"
            )


    # ======================================================
    # DISABLE USER
    # ======================================================

    @staticmethod
    def disable_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = (
            UserService
            ._now()
        )

        try:

            update_value(
                USER_MASTER,
                row_no,
                9,
                "INACTIVE"
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "User Disabled Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to disable user: {e}"
            )


    # ======================================================
    # SOFT DELETE
    # ======================================================

    @staticmethod
    def soft_delete_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = (
            UserService
            ._now()
        )

        try:

            update_value(
                USER_MASTER,
                row_no,
                9,
                "DELETED"
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "User Archived Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to archive user: {e}"
            )


    # ======================================================
    # CHANGE ROLE
    # ======================================================

    @staticmethod
    def change_role(
        row_no,
        role,
        modified_by="SYSTEM"
    ):

        role = str(
            role or ""
        ).strip()


        if role not in [
            ROLE_DEVELOPER,
            ROLE_ADMIN,
            ROLE_COORDINATOR
        ]:

            return (
                False,
                "Invalid user role."
            )


        current_time = (
            UserService
            ._now()
        )


        try:

            update_value(
                USER_MASTER,
                row_no,
                4,
                role
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "Role Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update role: {e}"
            )


    # ======================================================
    # CHANGE STATUS
    # ======================================================

    @staticmethod
    def change_status(
        row_no,
        status,
        modified_by="SYSTEM"
    ):

        status = str(
            status or ""
        ).strip().upper()


        if status not in [
            "ACTIVE",
            "INACTIVE",
            "DELETED"
        ]:

            return (
                False,
                "Invalid account status."
            )


        current_time = (
            UserService
            ._now()
        )


        try:

            update_value(
                USER_MASTER,
                row_no,
                9,
                status
            )

            update_value(
                USER_MASTER,
                row_no,
                16,
                current_time
            )

            update_value(
                USER_MASTER,
                row_no,
                17,
                modified_by
            )

            return (
                True,
                "Status Updated Successfully."
            )

        except Exception as e:

            return (
                False,
                f"Unable to update status: {e}"
            )


    # ======================================================
    # ROLE FILTER
    # ======================================================

    @staticmethod
    def get_users_by_role(
        role
    ):

        role = str(
            role or ""
        ).strip().lower()


        return [

            user

            for user in (
                UserService
                .get_all_users()
            )

            if str(
                user.get(
                    "Role",
                    ""
                )
            ).strip().lower()
            == role

            and str(
                user.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()
            != "DELETED"

        ]


    # ======================================================
    # ACTIVE USERS
    # ======================================================

    @staticmethod
    def get_active_users():

        return [

            user

            for user in (
                UserService
                .get_all_users()
            )

            if str(
                user.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()
            == "ACTIVE"

        ]


    # ======================================================
    # STATISTICS
    # ======================================================

    @staticmethod
    def statistics():

        users = (
            UserService
            .get_all_users()
        )


        active_users = [

            user

            for user in users

            if str(
                user.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()
            != "DELETED"

        ]


        return {

            "total":
                len(active_users),

            "developers":
                sum(
                    1
                    for user in active_users
                    if str(
                        user.get(
                            "Role",
                            ""
                        )
                    ).strip()
                    == ROLE_DEVELOPER
                ),

            "admins":
                sum(
                    1
                    for user in active_users
                    if str(
                        user.get(
                            "Role",
                            ""
                        )
                    ).strip()
                    == ROLE_ADMIN
                ),

            "coordinators":
                sum(
                    1
                    for user in active_users
                    if str(
                        user.get(
                            "Role",
                            ""
                        )
                    ).strip()
                    == ROLE_COORDINATOR
                )

        }


    # ======================================================
    # TOTAL USERS
    # ======================================================

    @staticmethod
    def total_users():

        return len(
            UserService
            .get_active_users()
        )


    # ======================================================
    # TOTAL BY ROLE
    # ======================================================

    @staticmethod
    def total_role(
        role
    ):

        return len(
            UserService
            .get_users_by_role(
                role
            )
        )
