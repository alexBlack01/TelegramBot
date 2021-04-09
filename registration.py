import logging
from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
import db_users
import main
import user

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

user = user.User()

val_sex = ['М', 'Ж']


class StageRegistration(StatesGroup):
    waiting_for_registration = State()
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_sex = State()
    waiting_for_sex_chosen = State()
    waiting_for_city = State()
    waiting_for_photo = State()


async def registration(message):
    user.set_id(message.from_user.id)

    await message.answer('Как тебя зовут?')
    await StageRegistration.waiting_for_name.set()


async def get_name(message: types.Message):
    name = message.text
    user.set_name(name)

    await message.answer('Сколько тебе лет?')
    await StageRegistration.waiting_for_age.set()


async def get_age(message: types.Message):
    age = message.text
    if not age.isdigit():
        await message.answer('Возраст должен быть цифрами, введите заново')
        await StageRegistration.waiting_for_age.set()
    else:
        age = int(age)
        user.set_age(age)
        await get_sex(message)


async def get_sex(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*val_sex)

    await message.answer('А какой у тебя пол?', reply_markup=keyboard)
    await StageRegistration.waiting_for_sex_chosen.set()


async def sex_chosen(message: types.Message):
    if message.text not in val_sex:
        await message.answer("Пожалуйста, выберите пол, используя клавиатуру ниже.")
        await StageRegistration.waiting_for_sex_chosen.set()
    else:
        sex = message.text
        user.set_sex(sex)

        await message.answer('В каком городе ты находишься?', reply_markup=types.ReplyKeyboardRemove())
        await StageRegistration.waiting_for_city.set()


async def get_city(message: types.Message):
    city = message.text
    user.set_city(city)

    await message.answer('Отсалось только загрузить фото')
    await StageRegistration.waiting_for_photo.set()


@dp.message_handler(content_types=['document'])
async def get_photo(message):
    #file_info = dp.get_file(message.document.file_id)
    #downloaded_file = bot.download_file(file_info.file_path)

    #src = 'C:\\Users\\asfsa\\Repository\\PI\\TelegramBot\\photos\\' + message.document.file_name
    #with open(src, 'wb') as new_file:
    #    new_file.write(downloaded_file)

    #user.set_photo(src)

    db_users.save_user_form(user)
    db_users.set_state(user.id, config.S_MENU)

    await main.base_menu(message)
