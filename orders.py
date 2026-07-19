from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from states import OrderState

router = Router()


# ==========================
# /zamow
# ==========================

@router.message(Command("zamow"))
async def start_order(message: Message, state: FSMContext):

    await state.set_state(OrderState.waiting_for_products)

    await message.answer(
        "🛒 <b>Składanie zamówienia</b>\n\n"
        "💵 Płatność wyłącznie gotówką.\n\n"
        "⚠️ Pojaw się około 5 minut przed ustaloną godziną.\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "📝 <b>Co chcesz zamówić?</b>\n\n"
        "Podaj ilość oraz produkty.",
        parse_mode="HTML"
    )


# ==========================
# PRODUKTY
# ==========================

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

    await state.set_state(OrderState.waiting_for_place)

    await message.answer(
        "📍 <b>Wybierz miejsce odbioru</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ==========================
# WYBÓR MIEJSCA
# ==========================

@router.callback_query(
    OrderState.waiting_for_place,
    F.data.startswith("place_")
)
async def place(callback: CallbackQuery, state: FSMContext):

    place = callback.data.replace("place_", "")

    await state.update_data(
        place=place
    )

    await state.set_state(OrderState.waiting_for_time)

    await callback.message.edit_text(
        "🕒 <b>Na którą godzinę?</b>\n\n"
        "Np. 18:30",
        parse_mode="HTML"
    )

    await callback.answer()