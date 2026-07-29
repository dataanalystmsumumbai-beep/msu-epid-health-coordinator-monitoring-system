from services.auth_service import AuthService
from core.session import login as create_session


def login(username, password):
    """
    Authenticate user and create session.
    Returns:
        (True, user) on success
        (False, error_message) on failure
    """

    status, result = AuthService.authenticate(username, password)

    if status:
        create_session(result)

    return status, result
