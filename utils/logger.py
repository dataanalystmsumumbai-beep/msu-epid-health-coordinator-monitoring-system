from utils.google_sheet import insert_row
from datetime import datetime


AUDIT_SHEET = "07_Audit_Log"

LOGIN_SHEET = "06_Login_History"


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
