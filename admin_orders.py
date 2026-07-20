from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from handlers import ADMINS
from orders import change_status
from database import (
    get_last_orders,
    get_orders_by_status,
    get_order,
    format_order_number
)

router = Router()


# =====================================
# HISTORIA ZAMÓWIEŃ
# =====================================

@router.message(Command("zamowienia"))
async def history(message: Message):

    if message.from_user.id not in ADMINS:
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟡 NOWE",
                    callback_data="list_NOWE"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟢 PRZYJĘTE",
                    callback_data="list_PRZYJĘTE"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 W REALIZACJI",
                    callback_data="list_W REALIZACJI"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 GOTOWE",
                    callback_data="list_GOTOWE"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ ODRZUCONE",
                    callback_data="list_ODRZUCONE"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 Wszystkie",
                    callback_data="list_all"
                )
            ]
        ]
    )

    await message.answer(
        "📚 <b>Panel historii zamówień</b>\n\nWybierz kategorię:",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =====================================
# POKAŻ ZAMÓWIENIE
# =====================================

@router.callback_query(F.data.startswith("show_"))
async def show_order(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    order_id = int(callback.data.split("_")[1])

    order = get_order(order_id)

    if not order:
        await callback.answer("Nie znaleziono.")
        return

    number = format_order_number(order_id)

    promo = "🎁 TAK" if order[11] else "❌ NIE"

    text = (
        f"📦 <b>{number}</b>\n\n"

        f"👤 {order[3]}\n"
        f"{order[2]}\n"
        f"<code>{order[1]}</code>\n\n"

        f"🎁 <b>Promocja</b>\n"
        f"{promo}\n\n"

        f"📦 {order[4]}\n\n"

        f"📍 {order[5]}\n"

        f"🕒 {order[6]}\n\n"

        f"📌 <b>{order[7]}</b>"
    )

    from keyboards import order_admin_keyboard

    keyboard = order_admin_keyboard(order_id)

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Historia",
                callback_data="back_orders"
            )
        ]
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()


# =====================================
# STATUSY
# =====================================

@router.callback_query(F.data.startswith("accepted_"))
async def accepted(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    await change_status(callback, "PRZYJĘTE", "🟢")


@router.callback_query(F.data.startswith("progress_"))
async def progress(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    await change_status(callback, "W REALIZACJI", "🚗")


@router.callback_query(F.data.startswith("ready_"))
async def ready(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    await change_status(callback, "GOTOWE", "📦")


@router.callback_query(F.data.startswith("cancel_"))
async def cancel(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    await change_status(callback, "ODRZUCONE", "❌")


# =====================================
# LISTA ZAMÓWIEŃ WG STATUSU
# =====================================

@router.callback_query(F.data.startswith("list_"))
async def show_list(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    value = callback.data.replace("list_", "")

    if value == "all":
        orders = get_last_orders()
    else:
        orders = get_orders_by_status(value)

    if not orders:
        await callback.answer("Brak zamówień.")
        return

    keyboard = []

    for order in orders:

        order_id = order[0]
        full_name = order[3]
        hour = order[6]
        status = order[7]

        if status == "NOWE":
            emoji = "🟡"
        elif status == "PRZYJĘTE":
            emoji = "🟢"
        elif status == "W REALIZACJI":
            emoji = "🚗"
        elif status == "GOTOWE":
            emoji = "📦"
        else:
            emoji = "❌"

        keyboard.append([
            InlineKeyboardButton(
                text=f"{format_order_number(order_id)} {emoji} {full_name} • {hour}",
                callback_data=f"show_{order_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Powrót",
            callback_data="back_orders"
        )
    ])

    titles = {
        "NOWE": "🟡 Nowe",
        "PRZYJĘTE": "🟢 Przyjęte",
        "W REALIZACJI": "🚗 W realizacji",
        "GOTOWE": "📦 Gotowe",
        "ODRZUCONE": "❌ Odrzucone",
        "all": "📚 Wszystkie"
    }

    title = titles.get(value, value)

    await callback.message.edit_text(
        f"📚 <b>{title}</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()


@router.callback_query(F.data == "back_orders")
async def back_orders(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟡 NOWE", callback_data="list_NOWE")],
            [InlineKeyboardButton(text="🟢 PRZYJĘTE", callback_data="list_PRZYJĘTE")],
            [InlineKeyboardButton(text="🚗 W REALIZACJI", callback_data="list_W REALIZACJI")],
            [InlineKeyboardButton(text="📦 GOTOWE", callback_data="list_GOTOWE")],
            [InlineKeyboardButton(text="❌ ODRZUCONE", callback_data="list_ODRZUCONE")],
            [InlineKeyboardButton(text="📚 Wszystkie", callback_data="list_all")]
        ]
    )

    await callback.message.edit_text(
        "📚 <b>Panel historii zamówień</b>\n\nWybierz kategorię:",
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await callback.answer()