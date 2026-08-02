if not username.strip() or not password:
    return False, "Username and Password are required."


from config.config import USER_MASTER

from utils.google_sheet import (
    read_all,
    update_value
)

from utils.security import verify_password

from utils.logger import (
    save_login_history,
    save_audit
)


class AuthService:

    @staticmethod
    def authenticate(username, password):

        username = username.strip().lower()

        users = read_all(USER_MASTER)

        for row_no, user in enumerate(users, start=2):

            db_username = str(
                user.get("Username", "")
            ).strip().lower()

            if db_username != username:
                continue

            # -------------------------
            # Status Check
            # -------------------------

            if str(
                user.get("Status", "ACTIVE")
            ).upper() != "ACTIVE":

                return False, "Account Disabled"

            # -------------------------
            # Locked Check
            # -------------------------

            if str(
                user.get("Account_Locked", "NO")
            ).upper() == "YES":

                return False, "Account Locked"

            # -------------------------
            # Password Verify
            # -------------------------

            password_hash = user.get(
                "Password_Hash",
                ""
            )

            if not verify_password(
                password,
                password_hash
            ):

           try:
    attempts = int(user.get("Login_Attempts", 0))
except:
    attempts = 0

attempts += 1

                update_value(
                    USER_MASTER,
                    row_no,
                    12,
                    attempts
                )

                if attempts >= 5:

                    update_value(
                        USER_MASTER,
                        row_no,
                        13,
                        "YES"
                    )

                    return False, "Account Locked"

                return False, "Invalid Password"

            # -------------------------
            # Reset Login Attempt
            # -------------------------

            update_value(
                USER_MASTER,
                row_no,
                12,
                0
            )

            update_value(
                USER_MASTER,
                row_no,
                10,
                "YES"
            )

            # -------------------------
            # Log
            # -------------------------

            save_login_history(user)

            save_audit(
                user,
                "LOGIN"
            )

            return True, user

        return False, "User Not Found"
