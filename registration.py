import config
import db_users
import main
import user
import keyboards

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

user = user.User()


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
        return
    else:
        age = int(age)
        if age <= 0 or age > 80:
            await message.answer('Столько люди не живут!')
            return
        else:
            user.set_age(age)
            await get_sex(message)


async def get_sex(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.keys_for_sex)

    await message.answer('А какой у тебя пол?', reply_markup=keyboard)
    await StageRegistration.waiting_for_sex_chosen.set()


async def sex_chosen(message: types.Message):
    if message.text not in keyboards.keys_for_sex:
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
    file_path = f'photos/{message.from_user.id}_photo.jpg'
    await message.photo[-1].download(destination=file_path)
    user.set_photo(file_path)

    db_users.save_user_form(user)
    db_users.set_state(user.id, config.S_MENU)

    await say_info(message)


async def say_info(message: types.Message):
    await message.answer('Основная регистрация профиля завершина!\n\n'
                         'Однако, чтобы воспользоваться дополнительными функциями поиска друзей, стоит пройти '
                         'дополнительную регистрацию.\n'
                         'Это можно сделать в любое время, когда тебе удобно.\n'
                         'Пока что тебе будет доступен просмотр всех анкет.')

    await main.create_notifications(message)
