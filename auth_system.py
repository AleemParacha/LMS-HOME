# auth_system.py
"""Group F - Authentication module."""

# Very simple in-memory user DB for demo/testing:
# Format: username -> {"password": str, "role": "librarian"|"member", "member_id": str|None}
DEFAULT_USER_DB = {
    "admin": {"password": "admin123", "role": "librarian", "member_id": None},
    # example member user: username "m1" with member_id "M001"
    "m1": {"password": "pass1", "role": "member", "member_id": "M001"},
}

def authenticate(username: str, password: str, user_db=None):
    """
    Authenticate user.

    Returns:
        tuple(bool, dict|None): (success, user_record)
    """
    if user_db is None:
        user_db = DEFAULT_USER_DB
    rec = user_db.get(username)
    if not rec:
        return False, None
    if rec.get("password") == password:
        return True, rec
    return False, None
