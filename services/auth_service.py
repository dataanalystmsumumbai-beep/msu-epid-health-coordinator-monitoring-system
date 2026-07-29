from utils.google_sheet import (
    read_all,
    update_value
)

from utils.security import verify_password

from utils.logger import (
    save_login_history,
    save_audit
)

USER_MASTER = "01_User_Master"


class AuthService:

    @staticmethod
    def authenticate(username, password):

        users = read_all(USER_MASTER)

        for index, user in enumerate(users, start=2):

            if str(user["Username"]).strip().lower() != username.strip().lower():
                continue

            if str(user["Status"]).upper() != "ACTIVE":
                return False, "Account Disabled"

            if str(user["Account_Locked"]).upper() == "YES":
                return False, "Account Locked"

            if not verify_password(
                password,
                user["Password_Hash"]
            ):

                attempts = int(user["Login_Attempts"]) + 1

                update_value(
                    USER_MASTER,
                    index,
                    12,
                    attempts
                )

                if attempts >= 5:

                    update_value(
                        USER_MASTER,
                        index,
                        13,
                        "YES"
                    )

                    return False, "Account Locked"

                return False, "Invalid Password"

            update_value(
                USER_MASTER,
                index,
                12,
                0
            )

            update_value(
                USER_MASTER,
                index,
                10,
                "YES"
            )

            save_login_history(user)

            save_audit(
                user,
                "LOGIN"
            )

            return True, user

        return False, "User Not Found"
