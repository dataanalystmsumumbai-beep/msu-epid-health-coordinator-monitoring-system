from utils.google_sheet import read_all


USER_MASTER = "01_User_Master"


def authenticate(username, password):

    users = read_all(USER_MASTER)

    for user in users:

        if str(user["Username"]).strip() != username.strip():
            continue

        if str(user["Password"]).strip() != password.strip():
            return False, "Wrong Password"

        if str(user["Status"]).upper() != "ACTIVE":
            return False, "User Inactive"

        return True, user

    return False, "User Not Found"
