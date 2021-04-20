
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers
import db_users


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()


async def regular_search(message: types.Message):
    user = db_users.db_regular_search
    print(user)
    print("Сюда заходили")
    await StageSearch.waiting_for_regular_search.set()


async def choose_doing(message: types.Message):
    return
