from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# Przycisk rozpoczynający weryfikację
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


# Przycisk akceptacji regulaminu
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


# Klawiatura z odpowiedziami do pytania
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


def get_all_users():
    cursor.execute(
        "SELECT user_id, verified, accepted_rules FROM users"
    )

    return cursor.fetchall()