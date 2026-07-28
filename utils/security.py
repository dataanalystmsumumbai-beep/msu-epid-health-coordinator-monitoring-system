import re

from config.config import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    ALLOWED_SPECIAL_CHARACTERS
)


def validate_password(password):

    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f"Minimum {PASSWORD_MIN_LENGTH} characters required."

    if len(password) > PASSWORD_MAX_LENGTH:
        return False, f"Maximum {PASSWORD_MAX_LENGTH} characters allowed."

    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one alphabet."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."

    special = "[" + re.escape(ALLOWED_SPECIAL_CHARACTERS) + "]"

    if not re.search(special, password):
        return False, "Password must contain at least one special character."

    invalid = "[^A-Za-z0-9" + re.escape(ALLOWED_SPECIAL_CHARACTERS) + "]"

    if re.search(invalid, password):
        return False, "Invalid special character used."

    return True, "Valid"
