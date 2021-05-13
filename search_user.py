import asyncio
import db_users
import main
import json

from types import SimpleNamespace
from bson import ObjectId
from emoji import emojize
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import queue_with_requests
from keyboards import keys_solution

storage = MemoryStorage()
loop_queue = asyncio.get_event_loop()


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()
    waiting_for_come_back = State()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def create_search_flow(message: types.Message):
    loop_queue.create_task(queue_with_requests.work_with_queue(message))
    await regular_search(message)


async def regular_search(message: types.Message):
    data = db_users.get_user_for_regular_search(message.from_user.id)
    data_json = JSONEncoder().encode(data)

    user = json.loads(data_json, object_hook=lambda d: SimpleNamespace(**d))
    caption = f'{user.form.name}, {user.form.age}, {user.form.city}'
    storage.user_id = message.from_user.id
    storage.form_id = user.user_id

    with open(user.form.photo, "rb") as file:
        data = file.read()

    await message.answer_photo(photo=data, caption=caption)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keys_solution)

    await message.answer(emojize(f'{keys_solution[0]} - Лайк\n'
                                 f'{keys_solution[1]} - Дизлайк\n'
                                 f'{keys_solution[2]} - Сон\n'
                                 f'{keys_solution[3]} - Изменить параметры\n', use_aliases=True),
                         reply_markup=keyboard)
    await StageSearch.waiting_for_regular_search.set()


async def regular_search_choose(message: types.Message):
    if message.text == keys_solution[0]:
        await message.answer('Реквест отправлен!')

        db_users.add_user_id_in_queue(storage.user_id, storage.form_id)
        db_users.add_user_to_whitelist(storage.user_id, storage.form_id)
        if db_users.check_user_in_list('blacklist', storage.user_id, storage.form_id):
            db_users.delete_user_from_blacklist(storage.user_id, storage.form_id)

        await regular_search(message)
    elif message.text == keys_solution[1]:
        await message.answer('Анкета пропущена!')

        db_users.add_user_to_blacklist(storage.user_id, storage.form_id)
        if db_users.check_user_in_list('whitelist', storage.user_id, storage.form_id):
            db_users.delete_user_from_whitelist(storage.user_id, storage.form_id)

        await regular_search(message)
    elif message.text == keys_solution[2]:
        await function_for_wait(message)

    elif message.text == keys_solution[3]:
        loop_queue.stop()
        await main.base_menu(message)

    else:
        await message.answer('Выбери что-то из предложенного!')
        return


async def function_for_wait(message: types.Message):
    await message.answer(emojize('Я буду ждать тебя! :cry:', use_aliases=True),
                         reply_markup=types.ReplyKeyboardRemove())

    await StageSearch.waiting_for_come_back.set()
