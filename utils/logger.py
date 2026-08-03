from utils.google_sheet import insert_row
from datetime import datetime


from config.config import (
    AUDIT_LOG,
    LOGIN_HISTORY
)

AUDIT_SHEET = AUDIT_LOG

LOGIN_SHEET = LOGIN_HISTORY


def save_login_history(user):

    insert_row(

        LOGIN_SHEET,

        [

            datetime.now().strftime("%d-%m-%Y"),

            datetime.now().strftime("%I:%M:%S %p"),

            user["User_ID"],

            user["Username"],

            user["Role"],

            "SUCCESS"

        ]

    )


def save_audit(user, action, remarks=""):

    insert_row(

        AUDIT_SHEET,

        [

            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),

            user["Username"],

            user["Role"],

            action,

            remarks

        ]

    )
