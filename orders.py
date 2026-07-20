import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from config import ADMIN_CHAT
from states import OrderState
from keyboards import order_admin_keyboard

from database import (
    get_user_orders,
    add_order,
    set_admin_message,
    update_order_status,
    get_order,
    format_order_number,
    set_order_price,
    get_order_price,
    get_orders_count
)

router = Router()


def format_products(text: str):

    items = re.split(r"[,\n]+", text)

    items = [item.strip() for item in items if item.strip()]

    return "\n".join(f"• {item}" for item in items)

# =====================================
# START ZAMÓWIENIA
# =====================================

@router.message(Command("zamow"))
async def start_order(message: Message, state: FSMContext):

    await state.clear()

    orders = get_orders_count(message.from_user.id)

    await state.set_state(OrderState.waiting_for_products)

    promo = ""
    promo_order = False

    if orders < 3:
        promo_order = True

        promo = (
            "🎁 <b>PROMOCJA DLA NOWYCH KLIENTÓW</b>\n\n"
            "Na Twoje pierwsze <b>3 zamówienia</b> obowiązują niższe ceny:\n\n"
            "⚡ Energetyk — <b>10 zł</b> (zamiast 15 zł)\n"
            "🚬 Papierosy klasyczne — <b>35 zł</b> (zamiast 45 zł)\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

    await state.update_data(
        promo=promo_order
    )

    await message.answer(

        "🛒 <b>Składanie zamówienia</b>\n\n"

        "📜 Korzystając z bota akceptujesz <b>regulamin</b>

        + promo +

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

    products = format_products(message.text)

    await state.update_data(
        products=products
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

    text = message.text.strip()

    # Jeśli użytkownik poda tylko godzinę, np. "14"
    if ":" not in text:
        text += ":00"

    match = re.fullmatch(r"(\d{1,2}):(\d{2})", text)

    if not match:
        await message.answer("❌ Niepoprawna godzina.")
        return

    hour = int(match.group(1))
    minute = int(match.group(2))

    if minute > 59:
        await message.answer("❌ Niepoprawna godzina.")
        return

    # Dozwolone godziny: 08:00–22:00
    if hour < 8 or hour > 22 or (hour == 22 and minute > 0):
        await message.answer(
            "❌ Zamówienia przyjmowane są wyłącznie w godzinach <b>08:00–22:00</b>.",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        order_time=text
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
        f"{text}\n\n"

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
        order_time=data["order_time"],
        promo=data["promo"]
    )

    number = format_order_number(order_id)

    promo = "🎁 TAK" if data["promo"] else "❌ NIE"

    admin_msg = await callback.bot.send_message(
        chat_id=ADMIN_CHAT,

        text=(
            f"🆕 <b>ZAMÓWIENIE {number}</b>\n\n"

            f"👤 <b>Klient</b>\n"
            f"{callback.from_user.full_name}\n"
            f"{username}\n"
            f"<code>{callback.from_user.id}</code>\n\n"

            f"🎁 <b>Promocja</b>\n"
            f"{promo}\n\n"

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
        f"<code>{number}</code>\n\n"

        "Administracja została powiadomiona.\n"
        "O zmianie statusu otrzymasz wiadomość.",

        parse_mode="HTML"
    )

    await state.clear()

    await callback.answer()


@router.callback_query(F.data.startswith("price_"))
async def ask_price(
    callback: CallbackQuery,
    state: FSMContext
):

    order_id = int(callback.data.split("_")[1])

    await state.update_data(
        price_order_id=order_id
    )

    await state.set_state(
        OrderState.waiting_for_price
    )

    await callback.message.answer(
        f"💰 Podaj cenę dla zamówienia <b>{format_order_number(order_id)}</b>",
        parse_mode="HTML"
    )

    await callback.answer()
# =====================================
# WSPÓLNA ZMIANA STATUSU
# =====================================


@router.message(OrderState.waiting_for_price)
async def save_price(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    order_id = data["price_order_id"]

    price = message.text.replace(",", ".")

    try:
        float(price)
    except ValueError:
        await message.answer("❌ Podaj poprawną cenę.")
        return

    set_order_price(order_id, price)

    order = get_order(order_id)

    if not order:
        await message.answer("❌ Nie znaleziono zamówienia.")
        await state.clear()
        return

    user_id = order[1]

    await message.answer(
        f"✅ Cena została ustawiona na: <b>{price} zł</b>",
        parse_mode="HTML"
    )

    try:
        await message.bot.send_message(
            user_id,
            f"💰 <b>Twoje zamówienie zostało wycenione.</b>\n\n"
            f"Do zapłaty: <b>{price} zł</b>\n\n"
            "Oczekuj na zmianę statusu zamówienia.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(e)

    await state.clear()


async def change_status(
    callback: CallbackQuery,
    status: str,
    emoji: str
):

    order_id = int(callback.data.split("_")[1])

    update_order_status(order_id, status)

    order = get_order(order_id)

    if not order:
        await callback.answer("Nie znaleziono zamówienia.")
        return

    number = format_order_number(order_id)

    user_id = order[1]
    username = order[2]
    full_name = order[3]
    products = order[4]
    place = order[5]
    order_time = order[6]

    # kolumna promo
    promo = "🎁 TAK" if order[11] else "❌ NIE"

    text = (
        f"🆕 <b>ZAMÓWIENIE {number}</b>\n\n"

        f"👤 <b>Klient</b>\n"
        f"{full_name}\n"
        f"{username}\n"
        f"<code>{user_id}</code>\n\n"

        f"🎁 <b>Promocja</b>\n"
        f"{promo}\n\n"

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
            f"📦 Zamówienie <b>{number}</b>\n\n"
            f"Status:\n"
            f"{emoji} <b>{status}</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(e)

    await callback.answer()


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
            f"<b>{format_order_number(order_id)}</b>\n"
            f"{emoji} {status}\n"
            f"📍 {place}\n"
            f"🕒 {hour}\n"
            f"📦 {products}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML"
    )
