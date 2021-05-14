import json
import config
import db_users
import keyboards
import search_user

from emoji import emojize
from types import SimpleNamespace
from bson import ObjectId
from aiogram import types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

storage = MemoryStorage()

bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class StageQueue(StatesGroup):
    waiting_for_queue = State()
    waiting_for_solution = State()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def work_with_queue(message: types.Message):
    have_doc_in_queue = True
    while have_doc_in_queue:
        if db_users.check_queue(message.from_user.id):
            have_doc_in_queue = False
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(*keyboards.keys_for_resolution)

            await message.answer('Есть люди, которых хотят с тобой познакомиться!\n'
                                 'Хотел бы ты взгянуть?', reply_markup=keyboard)

            await StageQueue.waiting_for_queue.set()


async def choose_var_queue(message: types.Message):
    if message.text not in keyboards.keys_for_resolution:
        await message.answer('Пожалуйста, выберите варинат, используя клавиатуру ниже.')
        return

    elif message.text == keyboards.keys_for_resolution[0]:
        await watching_queue(message)

    elif message.text == keyboards.keys_for_resolution[1]:
        await search_user.regular_search(message)


async def watching_queue(message: types.Message):
    queue = db_users.get_queue()
    for item in queue:
        data = db_users.get_user_by_id(item)
        data_json = JSONEncoder().encode(data)
        user = json.loads(data_json, object_hook=lambda d: SimpleNamespace(**d))
        caption = f'{user.form.name}, {user.form.age}, {user.form.city}'
        storage.user_id = message.from_user.id
        storage.form_id = user.user_id

        with open(user.form.photo, "rb") as file:
            data = file.read()

        await message.answer_photo(photo=data, caption=caption)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*keyboards.keys_solution)

        await message.answer(emojize(f'{keyboards.keys_solution[0]} - Лайк\n'
                                     f'{keyboards.keys_solution[1]} - Дизлайк\n'
                                     f'{keyboards.keys_solution[2]} - Сон\n'
                                     f'{keyboards.keys_solution[3]} - Изменить параметры\n', use_aliases=True),
                             reply_markup=keyboard)
        await StageQueue.waiting_for_solution.set()

    await search_user.regular_search(message)


async def regular_search_choose(message: types.Message):
    if message.text == keyboards.keys_solution[0]:
        data = db_users.get_username(message.from_user.id)
        data_json = JSONEncoder().encode(data)
        user = json.loads(data_json, object_hook=lambda d: SimpleNamespace(**d))
        await bot.send_message(storage.form_id, f'{user.username} Приятного общения!')

        data = db_users.get_username(storage.form_id)
        data_json = JSONEncoder().encode(data)
        user = json.loads(data_json, object_hook=lambda d: SimpleNamespace(**d))
        await message.answer(f'{user.username} Приятного общения!')

        db_users.delete_user_id_from_queue(storage.user_id, storage.form_id)
        db_users.add_user_to_whitelist(storage.user_id, storage.form_id)
        if db_users.check_user_in_list('blacklist', storage.user_id, storage.form_id):
            db_users.delete_user_from_blacklist(storage.user_id, storage.form_id)

    elif message.text == keyboards.keys_solution[1]:
        db_users.delete_user_id_from_queue(storage.user_id, storage.form_id)
        db_users.add_user_to_blacklist(storage.user_id, storage.form_id)
        if db_users.check_user_in_list('whitelist', storage.user_id, storage.form_id):
            db_users.delete_user_from_whitelist(storage.user_id, storage.form_id)

    else:
        await message.answer('Пожалуйста, выберите варинат, используя клавиатуру ниже.')
        return
