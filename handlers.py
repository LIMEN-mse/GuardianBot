from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards import start_keyboard
from verification import (
    start_verification,
    process_answer,
    process_rules
)

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