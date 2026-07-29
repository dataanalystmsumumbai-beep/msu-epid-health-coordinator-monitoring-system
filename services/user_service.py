from utils.google_sheet import read_all, append_row
from config.config import USER_MASTER

import hashlib
from datetime import datetime


class UserService:

    @staticmethod
    def get_all_users():
        return read_all(USER_MASTER)

    @staticmethod
    def create_user(
        username,
        password,
        role,
        full_name,
        designation,
        mobile,
        email,
        created_by="SYSTEM"
    ):

        users = read_all(USER_MASTER)

        # Username already exists?
        for user in users:
            if user["Username"].lower() == username.lower():
                return False, "Username already exists."

        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        user_id = f"USR{len(users)+1:03d}"

        row = [
            user_id,
            username,
            password_hash,
            role,
            full_name,
            designation,
            mobile,
            email,
            "ACTIVE",
            "",
            "YES",
            "0",
            "NO",
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            created_by,
            "",
            "",
            ""
        ]

        append_row(USER_MASTER, row)

        return True, "User Created Successfully"
