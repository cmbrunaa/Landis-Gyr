from database.database import get_connection


def save_validation(status, meter_model, meter_type, operator_name, created_at):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO validations (
            status,
            meter_model,
            meter_type,
            operator_name,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        status,
        meter_model,
        meter_type,
        operator_name,
        created_at
    ))

    validation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return validation_id

def save_divergences(validation_id, divergences):
    connection = get_connection()
    cursor = connection.cursor()

    for divergence in divergences:

        cursor.execute("""
            INSERT INTO divergences (
                validation_id,
                parameter,
                expected,
                found,
                message
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            validation_id,
            divergence["parameter"],
            divergence["expected"],
            divergence["found"],
            divergence["message"]
        ))

    connection.commit()
    connection.close()

def get_validations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            status,
            meter_model,
            meter_type,
            operator_name,
            created_at
        FROM validations
        ORDER BY id DESC
    """)

    validations = cursor.fetchall()

    connection.close()

    return validations

def get_divergences(validation_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            parameter,
            expected,
            found,
            message
        FROM divergences
        WHERE validation_id = ?
    """, (validation_id,))

    divergences = cursor.fetchall()

    connection.close()

    return divergences

def get_dashboard_summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM validations")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM validations WHERE status = 'CONFIRMADO'")
    confirmed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM validations WHERE status = 'REPROVADO'")
    reproved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM validations WHERE status = 'PENDENTE'")
    pending = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "confirmed": confirmed,
        "reproved": reproved,
        "pending": pending
    }

def get_validations_by_operator():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            operator_name,
            COUNT(*)
        FROM validations
        GROUP BY operator_name
        ORDER BY COUNT(*) DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data