import hashlib


# ==========================================================
# PASSWORD HASH
# ==========================================================

def hash_password(password: str) -> str:

    password = str(
        password or ""
    )

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==========================================================
# PASSWORD VERIFY
# ==========================================================

def verify_password(
    password: str,
    password_hash: str
) -> bool:

    password = str(
        password or ""
    )

    password_hash = str(
        password_hash or ""
    ).strip()


    if not password_hash:

        return False


    # ------------------------------------------------------
    # Standard SHA-256 verification
    # ------------------------------------------------------

    return (
        hash_password(password)
        == password_hash
    )


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

def validate_password(
    password: str,
    minimum_length: int = 8
):

    password = str(
        password or ""
    )


    if len(password) < minimum_length:

        return (
            False,
            f"Password must contain at least "
            f"{minimum_length} characters."
        )


    if password.strip() != password:

        return (
            False,
            "Password cannot start or end with spaces."
        )


    return (
        True,
        "Valid Password"
    )
