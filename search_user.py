import random
import config
import db_users
import main
import json

from types import SimpleNamespace
from bson import ObjectId
from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def regular_search(message: types.Message):
    data = db_users.get_all_users()
    data_json = JSONEncoder().encode(data)

    user = json.loads(data_json, object_hook=lambda d: SimpleNamespace(**d))
    caption = f'{user.form.name}, {user.form.age}, {user.form.city}'

    with open(user.form.photo, "rb") as file:
        data = file.read()

    await message.answer_photo(photo=data, caption=caption)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('1', '2', '3', '4')

    await message.answer('1 - Лайк\n'
                         '2 - Дизлайк\n'
                         '3 - Сон\n'
                         '4 - Изменить параметры', reply_markup=keyboard)

    await StageSearch.waiting_for_regular_search.set()


async def regular_search_choose(message: types.Message):
    if message.text == '1':
        await message.answer('Реквест отправлен!')
        await regular_search(message)
    if message.text == '2':
        await message.answer('Анкета пропущена!')
        await regular_search(message)
    if message.text == '3':
        await message.answer('Сон!')
        await regular_search(message)
    if message.text == '4':
        await main.base_menu(message)
    else:
        await message.answer('Выбери что-то из предложенного!')
        return
