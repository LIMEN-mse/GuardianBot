from datetime import datetime, timedelta, timezone

from aiogram import Bot
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import GROUP_ID, INVITE_LINK_DURATION
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

    # zapisanie zaakceptowania regulaminu
    accept_rules(user_id)

    bot: Bot = callback.bot

    # link ważny 25 minut
    expire_date = datetime.now(timezone.utc) + timedelta(
        seconds=INVITE_LINK_DURATION
    )

    # utworzenie jednorazowego linku
    invite = await bot.create_chat_invite_link(
        chat_id=GROUP_ID,
        expire_date=expire_date,
        member_limit=1,
        name=f"user_{user_id}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Dołącz do grupy",
                    url=invite.invite_link
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "✅ Regulamin zaakceptowany!\n\n"
        "🎟 Twój link jest jednorazowy.\n"
        "⏳ Jest ważny przez 25 minut.\n\n"
        "Kliknij przycisk poniżej, aby dołączyć do grupy.",
        reply_markup=keyboard
    )