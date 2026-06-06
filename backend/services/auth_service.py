from database.user_repository import find_user_by_username
from utils.password import verify_password


def login(username, password):
    user = find_user_by_username(username)

    if user is None:
        return None

    user_id, name, username_db, password_db, role = user

    if not verify_password(password, password_db):
        return None

    return {
        "id": user_id,
        "name": name,
        "username": username_db,
        "role": role
    }