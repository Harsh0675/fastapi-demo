from .database import get_db


def create_user(name: str, email: str):
    conn = get_db()

    try:
        cursor = conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return dict(row)

    finally:
        conn.close()


def get_users():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_user(user_id: int):
    conn = get_db()

    row = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def update_user(user_id: int, name: str, email: str):
    conn = get_db()

    cursor = conn.execute(
        """
        UPDATE users
        SET name = ?, email = ?
        WHERE id = ?
        """,
        (name, email, user_id)
    )

    conn.commit()

    row = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    conn.close()

    if cursor.rowcount == 0:
        return None

    return dict(row)


def delete_user(user_id: int):
    conn = get_db()

    cursor = conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return cursor.rowcount > 0
