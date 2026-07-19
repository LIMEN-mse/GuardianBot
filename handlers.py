from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import verify_keyboard
from aiogram import F
from aiogram.types import CallbackQuery

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🛡️ Witaj!\n\nKliknij przycisk poniżej.",
        reply_markup=verify_keyboard
    )


@router.callback_query(F.data == "verify")
async def verify(callback: CallbackQuery):
    await callback.answer("Zweryfikowano! 🎉")

    await callback.message.edit_text(
        "✅ Zweryfikowano!\n\nMiłego korzystania z bota 😎"
    )