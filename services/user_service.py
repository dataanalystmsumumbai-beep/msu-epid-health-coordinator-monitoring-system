from utils.google_sheet import read_all, insert_row
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

        username = username.strip()
        full_name = full_name.strip()
        designation = designation.strip()
        mobile = mobile.strip()
        email = email.strip()

        if username == "":
            return False, "Username is required."

        if password == "":
            return False, "Password is required."

        if full_name == "":
            return False, "Full Name is required."

        users = read_all(USER_MASTER)

        # Duplicate Username Check
        for user in users:

            if str(user.get("Username", "")).strip().lower() == username.lower():

                return False, "Username already exists."

        # Generate User ID
        user_id = f"USR{len(users)+1:03d}"

        # Password Hash
        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        row = [

            user_id,                  # User_ID
            full_name,                # Name
            username,                 # Username
            password_hash,            # Password_Hash
            role,                     # Role
            "",                       # Ward
            mobile,                   # Mobile
            "ACTIVE",                 # Status
            current_time,             # Created_On
            created_by                # Created_By

        ]

        insert_row(
            USER_MASTER,
            row
        )

        return True, "User Created Successfully."

    @staticmethod
    def get_user(username):

        users = read_all(USER_MASTER)

        for user in users:

            if str(user.get("Username", "")).lower() == username.lower():

                return user

        return None

    @staticmethod
    def username_exists(username):

        users = read_all(USER_MASTER)

        for user in users:

            if str(user.get("Username", "")).lower() == username.lower():

                return True

        return False

    @staticmethod
    def total_users():

        return len(
            read_all(USER_MASTER)
        )

    @staticmethod
    def total_role(role):

        users = read_all(USER_MASTER)

        count = 0

        for user in users:

            if str(user.get("Role", "")) == role:

                count += 1

        return count
