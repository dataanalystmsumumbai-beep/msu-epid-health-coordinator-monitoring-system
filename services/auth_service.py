from config.config import (
    USER_MASTER,
    MAX_LOGIN_ATTEMPTS
)

from utils.google_sheet import (
    read_all,
    update_value
)

from utils.security import (
    verify_password
)

from utils.logger import (
    save_login_history,
    save_audit
)


class AuthService:

    # ======================================================
    # AUTHENTICATE
    # ======================================================

    @staticmethod
    def authenticate(
        username,
        password
    ):

        username = str(
            username or ""
        ).strip().lower()

        password = str(
            password or ""
        )


        if not username or not password:

            return (
                False,
                "Username and Password are required."
            )


        try:

            users = (
                read_all(
                    USER_MASTER
                )
                or []
            )

        except Exception as e:

            return (
                False,
                f"Unable to read User Master: {e}"
            )


        for row_no, user in enumerate(
            users,
            start=2
        ):

            db_username = str(
                user.get(
                    "Username",
                    ""
                )
            ).strip().lower()


            if db_username != username:
                continue


            # ==================================================
            # ACCOUNT STATUS
            # ==================================================

            status = str(
                user.get(
                    "Status",
                    "ACTIVE"
                )
            ).strip().upper()


            if status != "ACTIVE":

                return (
                    False,
                    "Account Disabled"
                )


            # ==================================================
            # ACCOUNT LOCK
            # ==================================================

            locked = str(
                user.get(
                    "Account_Locked",
                    "NO"
                )
            ).strip().upper()


            if locked == "YES":

                return (
                    False,
                    "Account Locked. Contact an authorised administrator."
                )


            # ==================================================
            # PASSWORD
            # ==================================================

            password_hash = str(
                user.get(
                    "Password_Hash",
                    ""
                )
            ).strip()


            if not password_hash:

                return (
                    False,
                    "Password is not configured for this account."
                )


            try:

                valid_password = verify_password(
                    password,
                    password_hash
                )

            except Exception:

                valid_password = False


            # ==================================================
            # INVALID PASSWORD
            # ==================================================

            if not valid_password:

                try:

                    attempts = int(
                        user.get(
                            "Login_Attempts",
                            0
                        )
                    )

                except Exception:

                    attempts = 0


                attempts += 1


                update_value(
                    USER_MASTER,
                    row_no,
                    12,
                    attempts
                )


                if attempts >= MAX_LOGIN_ATTEMPTS:

                    update_value(
                        USER_MASTER,
                        row_no,
                        13,
                        "YES"
                    )


                    try:

                        save_audit(
                            user,
                            "ACCOUNT_LOCKED"
                        )

                    except Exception:
                        pass


                    return (
                        False,
                        "Account Locked"
                    )


                remaining = (
                    MAX_LOGIN_ATTEMPTS
                    - attempts
                )


                return (
                    False,
                    f"Invalid Password. "
                    f"{remaining} attempt(s) remaining."
                )


            # ==================================================
            # SUCCESS
            # ==================================================

            update_value(
                USER_MASTER,
                row_no,
                12,
                0
            )


            update_value(
                USER_MASTER,
                row_no,
                11,
                "YES"
            )


            # ==================================================
            # AUDIT / LOGIN HISTORY
            # ==================================================

            try:

                save_login_history(
                    user
                )

            except Exception:
                pass


            try:

                save_audit(
                    user,
                    "LOGIN"
                )

            except Exception:
                pass


            return (
                True,
                user
            )


        # ======================================================
        # USER NOT FOUND
        # ======================================================

        return (
            False,
            "User Not Found"
        )


    # ======================================================
    # LOGOUT
    # ======================================================

    @staticmethod
    def logout(user):

        if not user:
            return False


        try:

            save_audit(
                user,
                "LOGOUT"
            )

        except Exception:
            pass


        return True
