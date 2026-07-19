import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import router
from database import create_tables


print(f"TOKEN: {TOKEN}")
bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    create_tables()
    
    print("🚀 Bot wystartował!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
