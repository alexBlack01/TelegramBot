import config
import keyboards
import main
import user

from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

user = user.User()


class StageExtraRegistration(StatesGroup):
    waiting_for_extra_registration = State()
    waiting_for_get_music_info = State()
    waiting_for_get_movie_info = State()
    waiting_for_get_sex_info = State()
    waiting_for_get_zodiac_info = State()
    waiting_for_get_age_range_info = State()


async def extra_registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(5):
        keyboard.row(f'{i + 1}')
    keyboard.add(*keyboards.key_cancel)

    await message.answer('В дополнительной регистрации можно указать интересы и предпочтения по поиску:\n\n'
                         '1 - Указать музыкальные интересы\n'
                         '2 - Указать жанры кино\n'
                         '3 - Указать предпочтения по полу\n'
                         '4 - Указать предпочтения по знаку зодиака\n'
                         '5 - Указать предпочтения по возрасту\n'
                         'Назад - Вернуться в главное меню', reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_extra_registration.set()


async def choose_extra_registration(message: types.Message):
    if message.text == '1':
        await get_music_info(message)

    elif message.text == '2':
        await get_movie_info(message)

    elif message.text == '3':
        await get_sex_info(message)

    elif message.text == '4':
        await get_zodiac_info(message)

    elif message.text == '5':
        await get_age_range_info(message)

    elif message.text == 'Назад':
        await main.base_menu(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_music_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_cancel)

    await message.answer('Это функция музыки', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_music_info.set()


async def choose_music_info(message: types.Message):
    if message.text == 'Назад':
        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_movie_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_cancel)

    await message.answer('Это функция фильмов', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_movie_info.set()


async def choose_movie_info(message: types.Message):
    if message.text == 'Назад':
        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_sex_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_cancel)

    await message.answer('Это функция пола', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_sex_info.set()


async def choose_sex_info(message: types.Message):
    if message.text == 'Назад':
        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_zodiac_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_cancel)

    await message.answer('Это функция зодиака', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_zodiac_info.set()


async def choose_zodiac_info(message: types.Message):
    if message.text == 'Назад':
        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_age_range_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_cancel)

    await message.answer('Это функция возраста', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_age_range_info.set()


async def choose_age_range_info(message: types.Message):
    if message.text == 'Назад':
        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return
