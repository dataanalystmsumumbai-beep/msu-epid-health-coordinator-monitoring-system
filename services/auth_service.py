from datetime import datetime

from config.config import USERS

from utils.google_sheet import read_all

from utils.security import verify_password

from utils.logger import save_audit


class AuthService:

    # ==========================================================
    # GET ALL USERS
    # ==========================================================

    @staticmethod
    def get_all_users():

        try:

            data = read_all(
                USERS
            )

            return data if data else []

        except Exception:

            return []


    # ==========================================================
    # NORMALIZE ROLE
    # ==========================================================

    @staticmethod
    def normalize_role(role):

        role = str(
            role or ""
        ).strip().lower()


        role_map = {

            "developer": "Developer",

            "admin": "Admin",

            "administrator": "Admin",

            "coordinator": "Coordinator"

        }


        return role_map.get(
            role,
            ""
        )


    # ==========================================================
    # AUTHENTICATE
    # ==========================================================

    @staticmethod
    def authenticate(
        username,
        password
    ):

        username = str(
            username or ""
        ).strip()

        password = str(
            password or ""
        )


        if not username or not password:

            return (
                False,
                "Username and Password are required."
            )


        users = (
            AuthService
            .get_all_users()
        )


        for user in users:

            sheet_username = str(
                user.get(
                    "Username",
                    ""
                )
            ).strip()


            if (
                sheet_username.lower()
                != username.lower()
            ):

                continue


            status = str(
                user.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()


            if status not in [
                "ACTIVE",
                "ACTIVATED"
            ]:

                return (
                    False,
                    "Your account is inactive."
                )


            password_hash = str(
                user.get(
                    "Password_Hash",
                    user.get(
                        "Password",
                        ""
                    )
                )
            ).strip()


            if not verify_password(
                password,
                password_hash
            ):

                return (
                    False,
                    "Invalid Username or Password."
                )


            # --------------------------------------------------
            # NORMALIZE ROLE
            # --------------------------------------------------

            role = (
                AuthService
                .normalize_role(
                    user.get(
                        "Role",
                        ""
                    )
                )
            )


            if not role:

                return (
                    False,
                    "Invalid User Role."
                )


            user["Role"] = role


            # --------------------------------------------------
            # NORMALIZE USER VALUES
            # --------------------------------------------------

            user["Username"] = str(
                user.get(
                    "Username",
                    ""
                )
            ).strip()


            user["Full_Name"] = str(
                user.get(
                    "Full_Name",
                    user.get(
                        "Name",
                        ""
                    )
                )
            ).strip()


            user["User_ID"] = str(
                user.get(
                    "User_ID",
                    ""
                )
            ).strip()


            # --------------------------------------------------
            # LOGIN TIMESTAMP
            # --------------------------------------------------

            user["Last_Login"] = (
                datetime.now()
                .strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            )


            # --------------------------------------------------
            # AUDIT
            # --------------------------------------------------

            try:

                save_audit(
                    user,
                    "LOGIN",
                    "Successful login"
                )

            except Exception:

                pass


            return (
                True,
                user
            )


        return (
            False,
            "Invalid Username or Password."
        )
