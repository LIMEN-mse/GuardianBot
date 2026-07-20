from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ChatPermissions
)

from config import MUTE_TIME
from keyboards import (
    start_keyboard,
    admin_keyboard
)

from verification import (
    start_verification,
    process_answer,
    process_rules
)

from database import (
    get_total_users,
    get_verified_users,
    get_rules_users
)

router = Router()

# <<< TU WPISZ SWOJE ID TELEGRAMA >>>
ADMINS = [
    7470778133
]


# ===========================
# START
# ===========================

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🛡️ Witaj!\n\n"
        "Aby uzyskać dostęp do grupy, musisz przejść krótką weryfikację.",
        reply_markup=start_keyboard
    )


# ===========================
# WYŚWIETL SWOJE ID
# ===========================

@router.message(Command("id"))
async def my_id(message: Message):
    await message.answer(
        f"🆔 Twoje ID:\n\n<code>{message.from_user.id}</code>",
        parse_mode="HTML"
    )


# ===========================
# WERYFIKACJA
# ===========================

@router.callback_query(F.data == "start_verify")
async def start_verify(callback: CallbackQuery):
    await start_verification(callback)


@router.callback_query(F.data.startswith("answer_"))
async def answer(callback: CallbackQuery):
    await process_answer(callback)


@router.callback_query(F.data == "accept_rules")
async def accept(callback: CallbackQuery):
    await process_rules(callback)


# ===========================
# NOWY UŻYTKOWNIK
# ===========================

@router.message(F.new_chat_members)
async def new_member(message: Message):

    bot = message.bot

    for user in message.new_chat_members:

        if user.is_bot:
            continue

        try:

            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user.id,
                permissions=ChatPermissions(
                    can_send_messages=False
                )
            )

            await message.answer(
                f"👋 Witaj {user.full_name}!\n\n"
                "📖 Przez pierwsze 5 minut możesz tylko czytać czat.\n\n"
                "⏳ Po tym czasie możliwość pisania zostanie odblokowana automatycznie."
            )

            asyncio.create_task(
                unmute_user(
                    bot,
                    message.chat.id,
                    user.id
                )
            )

        except Exception as e:
            print(e)


async def unmute_user(bot, chat_id, user_id):

    await asyncio.sleep(MUTE_TIME)

    try:

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )

        await bot.send_message(
            chat_id,
            f"🔓 <a href='tg://user?id={user_id}'>Użytkownik</a> może już pisać.",
            parse_mode="HTML"
        )

    except Exception as e:
        print(e)




# ===========================
# DEBUG
# ===========================

# @router.message()
# async def debug(message: Message):
#     print("CHAT ID:", message.chat.id)


