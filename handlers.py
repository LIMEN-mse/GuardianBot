import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ChatPermissions
)

from keyboards import start_keyboard
from verification import (
    start_verification,
    process_answer,
    process_rules
)
from config import MUTE_TIME

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🛡️ Witaj!\n\n"
        "Aby uzyskać dostęp do grupy, musisz przejść krótką weryfikację.",
        reply_markup=start_keyboard
    )


@router.callback_query(F.data == "start_verify")
async def start_verify(callback: CallbackQuery):
    await start_verification(callback)


@router.callback_query(F.data.startswith("answer_"))
async def answer(callback: CallbackQuery):
    await process_answer(callback)


@router.callback_query(F.data == "accept_rules")
async def accept(callback: CallbackQuery):
    await process_rules(callback)


# Wykrycie nowego użytkownika w grupie
@router.message(F.new_chat_members)
async def new_member(message: Message):

    bot = message.bot

    for user in message.new_chat_members:

        if user.is_bot:
            continue

        # Zablokowanie pisania
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

        await message.answer(
            f"👋 Witaj {user.full_name}!\n\n"
            "📖 Przez pierwsze 5 minut możesz tylko czytać czat.\n"
            "⏳ Po 5 minutach możliwość pisania zostanie odblokowana automatycznie."
        )

        asyncio.create_task(
            unmute_user(bot, message.chat.id, user.id)
        )


async def unmute_user(bot, chat_id, user_id):

    await asyncio.sleep(MUTE_TIME)

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_invite_users=True
        )
    )

    await bot.send_message(
        chat_id,
        f"🔓 <a href='tg://user?id={user_id}'>Użytkownik</a> może już pisać na czacie!",
        parse_mode="HTML"
    )


@router.message()
async def debug(message: Message):
    print("CHAT ID:", message.chat.id)