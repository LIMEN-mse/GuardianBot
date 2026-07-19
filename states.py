from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    waiting_for_products = State()
    waiting_for_place = State()
    waiting_for_time = State()
    waiting_for_confirmation = State()