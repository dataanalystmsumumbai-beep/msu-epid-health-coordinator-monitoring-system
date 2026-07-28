from utils.google_sheet import append_row
from utils.datetime_utils import current_datetime


def save_audit_log(
    user,
    role,
    action,
    details
):

    append_row(

        "05_Audit_Log",

        [

            current_datetime(),

            user,

            role,

            action,

            details

        ]

    )
