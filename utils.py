import asyncio


async def wait(minutes):
    await asyncio.sleep(minutes * 60)