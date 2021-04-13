from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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

    await message.answer('Осталось только загрузить фото')
    await StageRegistration.waiting_for_photo.set()


async def get_photo(message: types.Message):
    await message.photo[-1].download()
    file_name = message.photo[-1].file_unique_id
    src = file_name

    # src = 'C:\\Users\\asfsa\\Repository\\PI\\TelegramBot\\photos\\' + message.document.file_name
    user.set_photo(src)

    db_users.save_user_form(user)
    db_users.set_state(user.id, config.S_MENU)

    await say_info(message)


async def say_info(message: types.Message):
    await message.answer('Основная регистрация профиля завершина!\n\n'
                         'Однако, чтобы воспользоваться дополнительными функциями поиска друзей, стоит пройти '
                         'дополнительную регистрацию.\n Ее можно пройти в любое время, когда тебе удобно.\n'
                         'Пока что тебе будет доступен просмотр всех анкет.')

    await main.base_menu(message)
