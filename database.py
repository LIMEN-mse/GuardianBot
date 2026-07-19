import sqlite3

db = sqlite3.connect("guardian.db")
cursor = db.cursor()


def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        verified INTEGER DEFAULT 0,
        accepted_rules INTEGER DEFAULT 0
    )
    """)

    db.commit()


def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )
    db.commit()


def verify_user(user_id):
    cursor.execute(
        "UPDATE users SET verified=1 WHERE user_id=?",
        (user_id,)
    )
    db.commit()


def accept_rules(user_id):
    cursor.execute(
        "UPDATE users SET accepted_rules=1 WHERE user_id=?",
        (user_id,)
    )
    db.commit()


def is_verified(user_id):
    cursor.execute(
        "SELECT verified FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    return bool(row and row[0])


def rules_accepted(user_id):
    cursor.execute(
        "SELECT accepted_rules FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    return bool(row and row[0])


def get_total_users():
    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    return cursor.fetchone()[0]


def get_verified_users():
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE verified=1"
    )
    return cursor.fetchone()[0]


def get_rules_users():
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE accepted_rules=1"
    )
    return cursor.fetchone()[0]


def get_all_users():
    cursor.execute(
        "SELECT user_id, verified, accepted_rules FROM users"
    )
    return cursor.fetchall()