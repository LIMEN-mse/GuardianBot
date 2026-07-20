from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from database import get_user_orders
from states import OrderState
from config import ADMIN_CHAT

from database import (
    add_order,
    set_admin_message,
    update_order_status,
    get_order
)

from keyboards import order_admin_keyboard

router = Router()


# =====================================
# START ZAMÓWIENIA
# =====================================

@router.message(Command("zamow"))
async def start_order(message: Message, state: FSMContext):

    await state.clear()

    await state.set_state(OrderState.waiting_for_products)

    await message.answer(
        "🛒 <b>Składanie zamówienia</b>\n\n"

        "💵 Płatność wyłącznie gotówką.\n\n"

        "⚠️ Na miejsce przyjdź około 5 minut wcześniej.\n\n"

        "❗ Niepojawienie się bez uzasadnienia może skutkować banem.\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "📦 <b>Co chcesz zamówić?</b>\n\n"

        "Podaj ilość oraz produkty.",

        parse_mode="HTML"
    )


# =====================================
# PRODUKTY
# =====================================

@router.message(OrderState.waiting_for_products)
async def products(message: Message, state: FSMContext):

    await state.update_data(
        products=message.text
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🏪 Dino",
                    callback_data="place_dino"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏪 Lewiatan",
                    callback_data="place_lewiatan"
                )
            ]

        ]
    )

    await state.set_state(
        OrderState.waiting_for_place
    )

    await message.answer(

        "📍 <b>Wybierz miejsce odbioru</b>",

        parse_mode="HTML",

        reply_markup=keyboard
    )


# =====================================
# WYBÓR MIEJSCA
# =====================================

@router.callback_query(
    OrderState.waiting_for_place,
    F.data.startswith("place_")
)
async def choose_place(
    callback: CallbackQuery,
    state: FSMContext
):

    place = callback.data.replace(
        "place_",
        ""
    )

    await state.update_data(
        place=place
    )

    await state.set_state(
        OrderState.waiting_for_time
    )

    await callback.message.edit_text(

        "🕒 <b>Na którą godzinę?</b>\n\n"

        "Przykład:\n"

        "<code>18:30</code>",

        parse_mode="HTML"
    )

    await callback.answer()


# =====================================
# GODZINA
# =====================================

@router.message(OrderState.waiting_for_time)
async def order_time(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        order_time=message.text
    )

    data = await state.get_data()

    place = (
        "🏪 Dino"
        if data["place"] == "dino"
        else "🏪 Lewiatan"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Potwierdź",
                    callback_data="confirm_order"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Anuluj",
                    callback_data="cancel_order"
                )
            ]
        ]
    )

    await state.set_state(
        OrderState.waiting_for_confirmation
    )

    await message.answer(

        "📋 <b>Podsumowanie</b>\n\n"

        f"📦 <b>Produkty</b>\n"
        f"{data['products']}\n\n"

        f"📍 <b>Miejsce</b>\n"
        f"{place}\n\n"

        f"🕒 <b>Godzina</b>\n"
        f"{data['order_time']}\n\n"

        "Czy wszystko się zgadza?",

        parse_mode="HTML",

        reply_markup=keyboard
    )


# =====================================
# POTWIERDZENIE ZAMÓWIENIA
# =====================================

@router.callback_query(
    OrderState.waiting_for_confirmation,
    F.data == "confirm_order"
)
async def confirm_order(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    place = (
        "🏪 Dino"
        if data["place"] == "dino"
        else "🏪 Lewiatan"
    )

    username = callback.from_user.username

    if username:
        username = f"@{username}"
    else:
        username = "Brak"

    order_id = add_order(
        user_id=callback.from_user.id,
        username=username,
        full_name=callback.from_user.full_name,
        products=data["products"],
        place=place,
        order_time=data["order_time"]
    )

    admin_msg = await callback.bot.send_message(
        chat_id=ADMIN_CHAT,

        text=(
            f"🆕 <b>ZAMÓWIENIE #{order_id:04d}</b>\n\n"

            f"👤 <b>Klient</b>\n"
            f"{callback.from_user.full_name}\n"
            f"{username}\n"
            f"<code>{callback.from_user.id}</code>\n\n"

            f"📦 <b>Produkty</b>\n"
            f"{data['products']}\n\n"

            f"📍 <b>Miejsce odbioru</b>\n"
            f"{place}\n\n"

            f"🕒 <b>Godzina</b>\n"
            f"{data['order_time']}\n\n"

            f"📌 <b>Status</b>\n"
            f"🟡 NOWE"
        ),

        parse_mode="HTML",

        reply_markup=order_admin_keyboard(order_id)
    )

    set_admin_message(
        order_id,
        admin_msg.message_id
    )

    await callback.message.edit_text(

        "✅ <b>Zamówienie zostało przyjęte.</b>\n\n"

        f"📦 Numer zamówienia:\n"
        f"<code>#{order_id:04d}</code>\n\n"

        "Administracja została powiadomiona.\n"
        "O zmianie statusu otrzymasz wiadomość.",

        parse_mode="HTML"
    )

    await state.clear()

    await callback.answer()


# =====================================
# WSPÓLNA ZMIANA STATUSU
# =====================================

async def change_status(
    callback: CallbackQuery,
    status: str,
    emoji: str
):

    order_id = int(
        callback.data.split("_")[1]
    )

    update_order_status(
        order_id,
        status
    )

    order = get_order(order_id)

    if not order:
        await callback.answer(
            "Nie znaleziono zamówienia."
        )
        return

    user_id = order[1]
    username = order[2]
    full_name = order[3]
    products = order[4]
    place = order[5]
    order_time = order[6]

    text = (
        f"🆕 <b>ZAMÓWIENIE #{order_id:04d}</b>\n\n"

        f"👤 <b>Klient</b>\n"
        f"{full_name}\n"
        f"{username}\n"
        f"<code>{user_id}</code>\n\n"

        f"📦 <b>Produkty</b>\n"
        f"{products}\n\n"

        f"📍 <b>Miejsce</b>\n"
        f"{place}\n\n"

        f"🕒 <b>Godzina</b>\n"
        f"{order_time}\n\n"

        f"📌 <b>Status</b>\n"
        f"{emoji} {status}"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=order_admin_keyboard(order_id)
    )

    try:
        await callback.bot.send_message(
            user_id,
            f"📦 Zamówienie <b>#{order_id:04d}</b>\n\n"
            f"Status:\n"
            f"{emoji} <b>{status}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(e)

    await callback.answer()


@router.callback_query(F.data.startswith("accepted_"))
async def accepted(callback: CallbackQuery):

    await change_status(
        callback,
        "PRZYJĘTE",
        "🟢"
    )


@router.callback_query(F.data.startswith("progress_"))
async def progress(callback: CallbackQuery):

    await change_status(
        callback,
        "W REALIZACJI",
        "🚗"
    )


@router.callback_query(F.data.startswith("ready_"))
async def ready(callback: CallbackQuery):

    await change_status(
        callback,
        "GOTOWE",
        "📦"
    )


@router.callback_query(F.data.startswith("cancel_"))
async def rejected(callback: CallbackQuery):

    await change_status(
        callback,
        "ODRZUCONE",
        "❌"
    )


# =====================================
# MOJE ZAMÓWIENIA
# =====================================

@router.message(Command("moje"))
async def my_orders(message: Message):

    orders = get_user_orders(
        message.from_user.id
    )

    if not orders:

        await message.answer(
            "📭 Nie masz jeszcze żadnych zamówień."
        )

        return

    text = "📦 <b>Twoje zamówienia</b>\n\n"

    for order in orders:

        order_id = order[0]
        products = order[1]
        place = order[2]
        hour = order[3]
        status = order[4]

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

        text += (
            f"<b>#{order_id:04d}</b>\n"
            f"{emoji} {status}\n"
            f"📍 {place}\n"
            f"🕒 {hour}\n"
            f"📦 {products}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML"
    )