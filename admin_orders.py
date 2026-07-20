from aiogram import Router, F
from aiogram.types import CallbackQuery

from orders import change_status

router = Router()


@router.callback_query(F.data.startswith("accepted_"))
async def accepted(callback: CallbackQuery):
    await change_status(callback, "PRZYJĘTE", "🟢")


@router.callback_query(F.data.startswith("progress_"))
async def progress(callback: CallbackQuery):
    await change_status(callback, "W REALIZACJI", "🚗")


@router.callback_query(F.data.startswith("ready_"))
async def ready(callback: CallbackQuery):
    await change_status(callback, "GOTOWE", "📦")


@router.callback_query(F.data.startswith("cancel_"))
async def cancel(callback: CallbackQuery):
    await change_status(callback, "ODRZUCONE", "❌")