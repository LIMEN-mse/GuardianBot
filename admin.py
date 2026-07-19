from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

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
# PANEL ADMINISTRATORA
# ===========================

@router.message(Command("panel"))
async def panel(message: Message):
    print(">>> PANEL WYKRYTY <<<")

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
        f"📜 Zaakceptowało regulamin: <b>{rules}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )


# ===========================
# STATYSTYKI
# ===========================

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer("Brak dostępu.", show_alert=True)
        return

    total = get_total_users()
    verified = get_verified_users()
    rules = get_rules_users()

    await callback.message.edit_text(
        f"📊 <b>Statystyki</b>\n\n"
        f"👥 Użytkowników: <b>{total}</b>\n"
        f"✅ Zweryfikowanych: <b>{verified}</b>\n"
        f"📜 Zaakceptowało regulamin: <b>{rules}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )

    await callback.answer()


# ===========================
# LISTA UŻYTKOWNIKÓW
# ===========================

@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer("Brak dostępu.", show_alert=True)
        return

    users = get_all_users()

    if not users:
        text = "👥 Brak użytkowników."
    else:
        text = "👥 <b>Lista użytkowników</b>\n\n"

        for user_id, verified, accepted in users:
            text += (
                f"🆔 <code>{user_id}</code>\n"
                f"✅ Zweryfikowany: {'TAK' if verified else 'NIE'}\n"
                f"📜 Regulamin: {'TAK' if accepted else 'NIE'}\n\n"
            )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )

    await callback.answer()


# ===========================
# OGŁOSZENIA
# ===========================

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer("Brak dostępu.", show_alert=True)
        return

    await callback.message.edit_text(
        "📢 Funkcja ogłoszeń pojawi się w kolejnej aktualizacji.",
        reply_markup=admin_keyboard
    )

    await callback.answer()