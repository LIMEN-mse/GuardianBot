from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# start_keyboard

# rules_keyboard

# question_keyboard()

# admin_keyboard

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