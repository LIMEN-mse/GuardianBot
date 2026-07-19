from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery
)

from keyboards import admin_keyboard

from database import (
    get_total_users,
    get_verified_users,
    get_rules_users,
    get_all_users
)

router = Router()

ADMINS = [
    7470778133
]


# ===========================
# /panel
# ===========================

@router.message(Command("panel"))
async def panel(message: Message):

    if message.from_user.id not in ADMINS:
        await message.answer("❌ Nie masz dostępu.")
        return

    total = get_total_users()
    verified = get_verified_users()
    rules = get_rules_users()

    await message.answer(
        f"🛡 <b>Guardian Panel</b>\n\n"
        f"👥 Użytkowników: <b>{total}</b>\n"
        f"✅ Zweryfikowanych: <b>{verified}</b>\n"
        f"📜 Regulamin zaakceptowało: <b>{rules}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )


# ===========================
# STATYSTYKI
# ===========================

@router.callback_query(F.data == "admin_stats")
async def stats(callback: CallbackQuery):

    total = get_total_users()
    verified = get_verified_users()
    rules = get_rules_users()

    await callback.message.edit_text(
        f"📊 <b>Statystyki</b>\n\n"
        f"👥 Użytkowników: <b>{total}</b>\n"
        f"✅ Zweryfikowanych: <b>{verified}</b>\n"
        f"📜 Regulamin zaakceptowało: <b>{rules}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )


# ===========================
# LISTA UŻYTKOWNIKÓW
# ===========================

@router.callback_query(F.data == "admin_users")
async def users(callback: CallbackQuery):

    users = get_all_users()

    if not users:

        text = "Brak użytkowników."

    else:

        text = "👥 <b>Lista użytkowników</b>\n\n"

        for user in users:

            uid, verified, rules = user

            text += (
                f"🆔 <code>{uid}</code>\n"
                f"✅ {'TAK' if verified else 'NIE'}\n"
                f"📜 {'TAK' if rules else 'NIE'}\n\n"
            )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )


# ===========================
# OGŁOSZENIA
# ===========================

@router.callback_query(F.data == "admin_broadcast")
async def broadcast(callback: CallbackQuery):

    await callback.message.edit_text(
        "📢 Funkcja ogłoszeń pojawi się w następnym etapie.",
        reply_markup=admin_keyboard
    )