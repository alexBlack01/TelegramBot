import random
import config
import db_users

from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from main import base_menu

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()


async def regular_search(message: types.Message):
    users = db_users.get_all_users()
    user = random.choice(users)

    caption = f'{user.name}, {user.age}, {user.city}'
    await bot.send_photo(message.from_user.id, photo=user.photo, caption=caption)

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
        await base_menu(message)
    else:
        await message.answer('Выбери что-то из предложенного!')
        return
