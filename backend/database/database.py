import sqlite3


DB_NAME = "first_off.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS validations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        meter_model TEXT,
        meter_type TEXT,
        operator_name TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS divergences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_id INTEGER NOT NULL,
            parameter TEXT NOT NULL,
            expected TEXT,
            found TEXT,
            message TEXT,
            FOREIGN KEY (validation_id) REFERENCES validations(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()