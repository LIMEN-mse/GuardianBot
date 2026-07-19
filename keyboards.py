from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


verify_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Zweryfikuj się",
                callback_data="verify"
            )
        ]
    ]
)