from datetime import datetime

from config.config import (
    LOGIN_HISTORY,
    AUDIT_LOG
)

from utils.google_sheet import (
    insert_row
)


# ==========================================================
# HELPERS
# ==========================================================

def _now():

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


def _value(
    row,
    *keys
):

    if not row:
        return ""

    for key in keys:

        value = row.get(
            key,
            ""
        )

        if value is not None:

            value = str(
                value
            ).strip()

            if value:
                return value

    return ""


# ==========================================================
# LOGIN HISTORY
# ==========================================================

def save_login_history(
    user,
    login_status="SUCCESS"
):

    if not user:
        return False


    row = [

        _now(),

        _value(
            user,
            "User_ID",
            "User_Id",
            "ID"
        ),

        _value(
            user,
            "Username",
            "User_Name"
        ),

        _value(
            user,
            "Role"
        ),

        login_status,

        "Streamlit Application"

    ]


    try:

        insert_row(
            LOGIN_HISTORY,
            row
        )

        return True

    except Exception:

        return False


# ==========================================================
# AUDIT LOG
# ==========================================================

def save_audit(
    user,
    action,
    details=""
):

    if not user:
        return False


    row = [

        _now(),

        _value(
            user,
            "User_ID",
            "User_Id",
            "ID"
        ),

        _value(
            user,
            "Username",
            "User_Name"
        ),

        _value(
            user,
            "Role"
        ),

        str(
            action or ""
        ).strip(),

        str(
            details or ""
        ).strip(),

        "Streamlit Application"

    ]


    try:

        insert_row(
            AUDIT_LOG,
            row
        )

        return True

    except Exception:

        return False


# ==========================================================
# GENERIC AUDIT ALIAS
# ==========================================================

def log_action(
    user,
    action,
    details=""
):

    return save_audit(
        user,
        action,
        details
    )


# ==========================================================
# LOGIN ALIAS
# ==========================================================

def log_login(
    user
):

    return save_login_history(
        user,
        "SUCCESS"
    )


# ==========================================================
# LOGOUT
# ==========================================================

def log_logout(
    user
):

    return save_audit(
        user,
        "LOGOUT"
    )
