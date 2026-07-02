import sqlite3
from contextlib import contextmanager

from models import encode_base62

DATABASE_NAME = "url_shortener.db"


@contextmanager
def get_db():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    try:

        yield connection

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def init_db():

    with get_db() as db:

        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            click_count INTEGER DEFAULT 0,
            expires_at TIMESTAMP NULL
        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_short_code
        ON urls(short_code)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id
        ON urls(user_id)
        """)


def create_user(email, hashed_password):

    with get_db() as db:

        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO users(email, password)
            VALUES(?, ?)
            """,
            (email, hashed_password)
        )

        return cursor.lastrowid


def get_user_by_email(email):

    with get_db() as db:

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)


def create_url(long_url, user_id=None):

    with get_db() as db:

        cursor = db.cursor()

        #
        # Step 1
        # Insert placeholder
        #

        cursor.execute(
            """
            INSERT INTO urls(long_url, user_id, short_code)
            VALUES(?, ?, '')
            """,
            (long_url, user_id)
        )

        url_id = cursor.lastrowid

        short_code = encode_base62(url_id)

        #
        # Step 2
        # Update generated code
        #

        cursor.execute(
            """
            UPDATE urls
            SET short_code = ?
            WHERE id = ?
            """,
            (
                short_code,
                url_id
            )
        )

        return short_code


def get_url(short_code: str):
    """Retrieve URL record without side effects."""
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
        row = cursor.fetchone()
        return dict(row) if row else None


def increment_click(short_code: str) -> None:
    """Increment click count. Called only by the redirect route."""
    with get_db() as db:
        db.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
            (short_code,),
        )

def get_urls_for_user(user_id):

    with get_db() as db:

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT *
            FROM urls
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


if __name__ == "__main__":

    init_db()

    print("Database initialized.")