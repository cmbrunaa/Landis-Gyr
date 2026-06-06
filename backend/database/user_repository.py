from database.database import get_connection


def create_user(name, username, password, role, created_at):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (
            name,
            username,
            password,
            role,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        username,
        password,
        role,
        created_at
    ))

    connection.commit()
    connection.close()


def find_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            username,
            password,
            role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    connection.close()

    return user


def list_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            username,
            role,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    connection.close()

    return users