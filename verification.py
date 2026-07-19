from aiogram.types import CallbackQuery

from questions import QUESTIONS
from rules import RULES
from keyboards import (
    question_keyboard,
    rules_keyboard
)
from database import (
    add_user,
    verify_user,
    accept_rules
)


# Zapamiętuje, na którym pytaniu jest użytkownik
user_progress = {}


async def start_verification(callback: CallbackQuery):
    user_id = callback.from_user.id

    add_user(user_id)

    user_progress[user_id] = 0

    question = QUESTIONS[0]

    await callback.message.edit_text(
        f"❓ {question['question']}",
        reply_markup=question_keyboard(question)
    )


async def process_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_progress:
        return

    question_index = user_progress[user_id]

    question = QUESTIONS[question_index]

    answer = int(callback.data.split("_")[1])

    if answer != question["correct"]:
        await callback.answer(
            "❌ Zła odpowiedź!",
            show_alert=True
        )
        return

    question_index += 1

    if question_index >= len(QUESTIONS):

        verify_user(user_id)

        await callback.message.edit_text(
            RULES,
            reply_markup=rules_keyboard
        )

        return

    user_progress[user_id] = question_index

    question = QUESTIONS[question_index]

    await callback.message.edit_text(
        f"❓ {question['question']}",
        reply_markup=question_keyboard(question)
    )


async def process_rules(callback: CallbackQuery):
    user_id = callback.from_user.id

    accept_rules(user_id)

    await callback.message.edit_text(
        "✅ Weryfikacja zakończona!\n\nZa chwilę otrzymasz dostęp do serwera."
    )