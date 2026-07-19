import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import router
from database import create_tables


# Debug
print("TOKEN:", repr(TOKEN))
print("TOKEN LENGTH:", len(TOKEN) if TOKEN else "BRAK TOKENA")

bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    create_tables()

    print("🚀 Bot wystartował!")

    # Sprawdzenie czy Telegram akceptuje token
    me = await bot.get_me()
    print(f"✅ Zalogowano jako: @{me.username} ({me.id})")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())