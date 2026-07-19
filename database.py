import sqlite3

db = sqlite3.connect("data.db")
cursor = db.cursor()


def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        verified INTEGER DEFAULT 0
    )
    """)

    db.commit()


def add_user(user_id, username, first_name):
    cursor.execute("""
    INSERT OR IGNORE INTO users(user_id, username, first_name)
    VALUES (?, ?, ?)
    """, (user_id, username, first_name))

    db.commit()


def verify_user(user_id):
    cursor.execute("""
    UPDATE users
    SET verified = 1
    WHERE user_id = ?
    """, (user_id,))

    db.commit()