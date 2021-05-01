
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers
import db_users


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()


async def regular_search(message: types.Message):
    users = db_users.get_all_users()
    print(users)
    print("Сюда заходили")
    await StageSearch.waiting_for_regular_search.set()


async def choose_doing(message: types.Message):
    return
