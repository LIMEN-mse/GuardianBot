from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==========================
# START
# ==========================

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛡 Rozpocznij weryfikację",
                callback_data="start_verify"
            )
        ]
    ]
)


# ==========================
# REGULAMIN
# ==========================

rules_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Akceptuję regulamin",
                callback_data="accept_rules"
            )
        ]
    ]
)


# ==========================
# PYTANIA
# ==========================

def question_keyboard(question):
    keyboard = []

    for i, answer in enumerate(question["answers"]):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"answer_{i}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )


# ==========================
# PANEL ADMINA
# ==========================

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Statystyki",
                callback_data="admin_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Lista użytkowników",
                callback_data="admin_users"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Ogłoszenie",
                callback_data="admin_broadcast"
            )
        ]
    ]
)


# ==========================
# PANEL ZAMÓWIEŃ
# ==========================

def order_admin_keyboard(order_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Przyjęte",
                    callback_data=f"accepted_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 W realizacji",
                    callback_data=f"progress_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Gotowe",
                    callback_data=f"ready_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Odrzuć",
                    callback_data=f"cancel_{order_id}"
                )
            ]
        ]
    )