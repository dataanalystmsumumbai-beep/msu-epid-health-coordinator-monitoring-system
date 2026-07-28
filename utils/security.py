import re


ALLOWED_SPECIAL_CHARACTERS = "@#$-._"


def validate_password(password: str):

    if len(password) < 8 or len(password) > 10:
        return False, "Password must be between 8 and 10 characters."

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

    return True, "Valid Password"
