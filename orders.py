from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

print("✅ ORDERS.PY ZAŁADOWANY")

router = Router()


@router.message(Command("zamow"))
async def order(message: Message):

    await message.answer(
        "🛒 Rozpoczynamy składanie zamówienia!\n\n"
        "💵 Płatność wyłącznie gotówką.\n\n"
        "⚠️ Pojaw się około 5 minut przed umówioną godziną.\n\n"
        "W następnym kroku bot zapyta Cię o produkty."
    )