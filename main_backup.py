from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

TOKEN = "8866573034:AAEg_h6q4kDMTGSr7uOeMSgPWCrR-lfar4c"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Cześć! Bot działa!")


async def main():
    print("Bot się uruchamia...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Start programu")
    asyncio.run(main())