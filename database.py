import sqlite3
import os

print("DB PATH:", os.path.abspath("guardian.db"))

db = sqlite3.connect("guardian.db")
cursor = db.cursor()


# ==========================================
# TWORZENIE TABEL
# ==========================================

def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    verified INTEGER DEFAULT 0,
    accepted_rules INTEGER DEFAULT 0,
    started INTEGER DEFAULT 0,
    promo_orders INTEGER DEFAULT 0
)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    full_name TEXT,
    products TEXT NOT NULL,
    place TEXT NOT NULL,
    order_time TEXT NOT NULL,
    status TEXT DEFAULT 'NOWE',
    price TEXT,
    admin_message_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    """)

    db.commit()

try:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN promo_orders INTEGER DEFAULT 0"
    )
    db.commit()
except:
    pass

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN price TEXT")
    db.commit()
except:
    pass

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN promo INTEGER DEFAULT 0")
    db.commit()
except:
    pass

# ==========================================
# UŻYTKOWNICY
# ==========================================

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


# ==========================================
# ZAMÓWIENIA
# ==========================================

def add_order(
    user_id,
    username,
    full_name,
    products,
    place,
    order_time,
    promo
):

    cursor.execute(
        """
        INSERT INTO orders(
            user_id,
            username,
            full_name,
            products,
            place,
            order_time,
            promo
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            user_id,
            username,
            full_name,
            products,
            place,
            order_time,
            int(promo)
        )
    )

    db.commit()

    return cursor.lastrowid


def get_order(order_id):

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE id=?
        """,
        (order_id,)
    )

    return cursor.fetchone()


def get_all_orders():

    cursor.execute(
        """
        SELECT *
        FROM orders
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()


def get_user_orders(user_id):

    cursor.execute(
        """
        SELECT
            id,
            products,
            place,
            order_time,
            status,
            created_at
        FROM orders
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    return cursor.fetchall()


def update_order_status(order_id, status):

    cursor.execute(
        """
        UPDATE orders
        SET status=?
        WHERE id=?
        """,
        (
            status,
            order_id
        )
    )

    db.commit()


def set_admin_message(order_id, message_id):

    cursor.execute(
        """
        UPDATE orders
        SET admin_message_id=?
        WHERE id=?
        """,
        (
            message_id,
            order_id
        )
    )

    db.commit()


def format_order_number(order_id):

    return f"LMN-{order_id:04d}"


def has_started(user_id):

    cursor.execute(
        """
        SELECT started
        FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    if not row:
        return False

    return bool(row[0])


def set_started(user_id):

    cursor.execute(
        """
        UPDATE users
        SET started=1
        WHERE user_id=?
        """,
        (user_id,)
    )

    db.commit()


def set_order_price(order_id, price):

    cursor.execute(
        """
        UPDATE orders
        SET price=?
        WHERE id=?
        """,
        (price, order_id)
    )

    db.commit()


def get_order_price(order_id):

    cursor.execute(
        """
        SELECT price
        FROM orders
        WHERE id=?
        """,
        (order_id,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    return row[0]


def get_orders_count(user_id):

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM orders
        WHERE user_id=?
        """,
        (user_id,)
    )

    return cursor.fetchone()[0]


def get_last_orders(limit=20):

    cursor.execute(
        """
        SELECT *
        FROM orders
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    return cursor.fetchall()


def get_orders_by_status(status):

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE status=?
        ORDER BY id DESC
        """,
        (status,)
    )

    return cursor.fetchall()


def get_promo_orders(user_id):

    cursor.execute("""
        SELECT promo_orders
        FROM users
        WHERE user_id=?
    """, (user_id,))

    row = cursor.fetchone()

    if not row:
        return 0

    return row[0]


def increase_promo_orders(user_id):

    cursor.execute("""
        UPDATE users
        SET promo_orders = promo_orders + 1
        WHERE user_id=?
    """, (user_id,))

    print("Rows updated:", cursor.rowcount)

    db.commit()


def user_exists(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )
    print(cursor.fetchone())
