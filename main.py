import asyncio

from aiogram import Bot, Dispatcher
from admin import router as admin_router
from config import TOKEN
from handlers import router
from database import create_tables

bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_router(router)
dp.include_router(admin_router)

async def main():
    create_tables()

    print("🚀 Bot wystartował!")

    me = await bot.get_me()
    print(f"✅ Zalogowano jako @{me.username}")

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    asyncio.run(main())