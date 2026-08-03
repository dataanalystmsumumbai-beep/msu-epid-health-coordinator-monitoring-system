from datetime import datetime
import hashlib

from config.config import USER_MASTER
from utils.google_sheet import (
    read_all,
    insert_row,
    update_value
)


class UserService:

    @staticmethod
    def get_all_users():
        """
        Returns all users from User Master sheet.
        """
        return read_all(USER_MASTER)

    @staticmethod
    def get_user(username):
        """
        Get user by username.
        """

        if not username:
            return None

        users = read_all(USER_MASTER)

        for user in users:

            if (
                str(user.get("Username", "")).strip().lower()
                ==
                username.strip().lower()
            ):
                return user

        return None

    @staticmethod
    def username_exists(username):

        return UserService.get_user(username) is not None

    @staticmethod
    def generate_user_id():

        users = read_all(USER_MASTER)

        max_id = 0

        for user in users:

            uid = str(user.get("User_ID", "")).replace("USR", "")

            try:
                max_id = max(max_id, int(uid))
            except:
                pass

        return f"USR{max_id + 1:03d}"

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
        password = password.strip()
        role = role.strip()
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

        if UserService.username_exists(username):
            return False, "Username already exists."

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        row = [

            UserService.generate_user_id(),     # User_ID
            username,                           # Username
            password_hash,                      # Password_Hash
            role,                               # Role
            full_name,                          # Full_Name
            designation,                        # Designation
            mobile,                             # Mobile
            email,                              # Email
            "ACTIVE",                           # Status
            "",                                 # Last_Login
            current_time,                       # Password_Changed
            0,                                  # Login_Attempts
            "NO",                               # Account_Locked
            current_time,                       # Created_On
            created_by,                         # Created_By
            "",                                 # Modified_On
            "",                                 # Modified_By
            ""                                  # Remarks

        ]

        insert_row(
            USER_MASTER,
            row
        )

        return True, "User Created Successfully."

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

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        update_value(USER_MASTER, row_no, 4, role)
        update_value(USER_MASTER, row_no, 5, full_name)
        update_value(USER_MASTER, row_no, 6, designation)
        update_value(USER_MASTER, row_no, 7, mobile)
        update_value(USER_MASTER, row_no, 8, email)
        update_value(USER_MASTER, row_no, 16, current_time)
        update_value(USER_MASTER, row_no, 17, modified_by)

        return True, "User Updated Successfully."

    @staticmethod
    def lock_user(row_no):

        update_value(USER_MASTER, row_no, 13, "YES")

        return True, "User Locked Successfully."

    @staticmethod
    def unlock_user(row_no):

        update_value(USER_MASTER, row_no, 13, "NO")
        update_value(USER_MASTER, row_no, 12, 0)

        return True, "User Unlocked Successfully."

    @staticmethod
    def reset_password(
        row_no,
        new_password,
        modified_by="SYSTEM"
    ):

        password_hash = hashlib.sha256(
            new_password.encode("utf-8")
        ).hexdigest()

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        update_value(USER_MASTER, row_no, 3, password_hash)
        update_value(USER_MASTER, row_no, 11, current_time)
        update_value(USER_MASTER, row_no, 12, 0)
        update_value(USER_MASTER, row_no, 13, "NO")
        update_value(USER_MASTER, row_no, 16, current_time)
        update_value(USER_MASTER, row_no, 17, modified_by)

        return True, "Password Reset Successfully."

    @staticmethod
    def disable_user(
        row_no,
        modified_by="SYSTEM"
    ):

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        update_value(USER_MASTER, row_no, 9, "INACTIVE")
        update_value(USER_MASTER, row_no, 16, current_time)
        update_value(USER_MASTER, row_no, 17, modified_by)

        return True, "User Disabled Successfully."

    @staticmethod
    def total_users():

        return len(read_all(USER_MASTER))

    @staticmethod
    def total_role(role):

        users = read_all(USER_MASTER)

        return sum(
            1
            for user in users
            if str(user.get("Role", "")).strip() == role
        )
        
    @staticmethod
    def statistics():

        users = read_all(USER_MASTER)

        return {

            "total": len(users),

            "developers": sum(
                1
                for u in users
                if str(u.get("Role", "")) == "Developer"
            ),

            "admins": sum(
                1
                for u in users
                if str(u.get("Role", "")) == "Admin"
            ),

            "coordinators": sum(
                1
                for u in users
                if str(u.get("Role", "")) == "Coordinator"
            )

        }
