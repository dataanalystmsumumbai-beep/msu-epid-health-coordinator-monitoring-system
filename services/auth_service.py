from utils.google_sheet import read_all

USER_MASTER = "01_User_Master"


class AuthService:

    @staticmethod
    def get_user(username):

        users = read_all(USER_MASTER)

        for user in users:

            if str(user["Username"]).strip().lower() == username.strip().lower():

                return user

        return None
