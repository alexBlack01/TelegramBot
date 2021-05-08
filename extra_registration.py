import keyboards
import main
import user
from emoji import emojize
import db_users

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

user = user.UserExtra()


class StageExtraRegistration(StatesGroup):
    waiting_for_extra_registration = State()
    waiting_for_get_music_info = State()
    waiting_for_get_movie_info = State()
    waiting_for_get_sex_info = State()
    waiting_for_get_zodiac_info = State()
    waiting_for_get_age_range_info = State()


async def extra_registration(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*keyboards.keys_for_extra_registration)
    keyboard.add(keyboards.key_save_and_cancel[1])

    await message.answer(emojize('В дополнительной регистрации можно указать интересы и предпочтения по поиску:\n'
                                 f'{keyboards.keys_for_extra_registration[0]} - Указать музыкальные интересы\n'
                                 f'{keyboards.keys_for_extra_registration[1]} - Указать жанры кино\n'
                                 f'{keyboards.keys_for_extra_registration[2]} - Указать предпочтения по полу\n'
                                 f'{keyboards.keys_for_extra_registration[3]} - Указать предпочтения по знаку зодиака\n'
                                 f'{keyboards.keys_for_extra_registration[4]} - Указать предпочтения по возрасту\n'
                                 f'{keyboards.key_save_and_cancel[1]} - Вернуться в главное меню', use_aliases=True),
                         reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_extra_registration.set()


async def choose_extra_registration(message: types.Message):
    if message.text == keyboards.keys_for_extra_registration[0]:
        await get_music_info(message)

    elif message.text == keyboards.keys_for_extra_registration[1]:
        await get_movie_info(message)

    elif message.text == keyboards.keys_for_extra_registration[2]:
        await get_sex_info(message)

    elif message.text == keyboards.keys_for_extra_registration[3]:
        await get_zodiac_info(message)

    elif message.text == keyboards.keys_for_extra_registration[4]:
        await get_age_range_info(message)

    elif message.text == keyboards.key_save_and_cancel[1]:
        await main.base_menu(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_music_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(2):
        keyboard.row(keyboards.keys_music[4 * i], keyboards.keys_music[4 * i + 1],
                     keyboards.keys_music[4 * i + 2], keyboards.keys_music[4 * i + 3])
    keyboard.row(*keyboards.key_save_and_cancel)

    await message.answer(emojize('Выбери жанры музыки, которые любишь:\n'
                                 f'{keyboards.keys_music[0]} - Инди\n'
                                 f'{keyboards.keys_music[1]} - Поп\n'
                                 f'{keyboards.keys_music[2]} - Хип-хоп\n'
                                 f'{keyboards.keys_music[3]} - Классика\n'
                                 f'{keyboards.keys_music[4]} - Рок\n'
                                 f'{keyboards.keys_music[5]} - Шансон\n'
                                 f'{keyboards.keys_music[6]} - Джаз\n'
                                 f'{keyboards.keys_music[7]} - Фолк\n'
                                 f'{keyboards.key_save_and_cancel[0]} - Сохранить ответы\n'
                                 f'{keyboards.key_save_and_cancel[1]} - Вернуться назад', use_aliases=True),
                         reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_get_music_info.set()


async def choose_music_info(message: types.Message):
    if message.text in keyboards.keys_music:
        if message.text not in user.music:
            user.set_music(message.text)

        await StageExtraRegistration.waiting_for_get_music_info.set()

    elif message.text in keyboards.key_save_and_cancel:
        if message.text == keyboards.key_save_and_cancel[0]:
            db_users.save_music_info(message.from_user.id, user.music)

        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_movie_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(3):
        keyboard.row(keyboards.keys_movie[3 * i], keyboards.keys_movie[3 * i + 1], keyboards.keys_movie[3 * i + 2])
    keyboard.add(*keyboards.key_save_and_cancel)

    await message.answer(emojize('Выбери жанры кино, которые любишь:\n'
                                 f'{keyboards.keys_movie[0]} - Хоррор\n'
                                 f'{keyboards.keys_movie[1]} - Фантастика\n'
                                 f'{keyboards.keys_movie[2]} - Драма\n'
                                 f'{keyboards.keys_movie[3]} - Экшн\n'
                                 f'{keyboards.keys_movie[4]} - Детектив\n'
                                 f'{keyboards.keys_movie[5]} - Биография\n'
                                 f'{keyboards.keys_movie[6]} - Боевик\n'
                                 f'{keyboards.keys_movie[7]} - Детское\n'
                                 f'{keyboards.keys_movie[8]} - Историческое\n'
                                 f'{keyboards.key_save_and_cancel[0]} - Сохранить ответы\n'
                                 f'{keyboards.key_save_and_cancel[1]} - Вернуться назад', use_aliases=True),
                         reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_get_movie_info.set()


async def choose_movie_info(message: types.Message):
    if message.text in keyboards.keys_movie:
        if message.text not in user.movie:
            user.set_movie(message.text)

        await StageExtraRegistration.waiting_for_get_movie_info.set()

    elif message.text in keyboards.key_save_and_cancel:
        if message.text == keyboards.key_save_and_cancel[0]:
            db_users.save_movie_info(message.from_user.id, user.movie)

        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_sex_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*keyboards.keys_for_sex, keyboards.key_no_sex)
    keyboard.row(*keyboards.key_save_and_cancel)

    await message.answer('Выбери пол собеседника, которого хочешь найти:\n'
                         f'{keyboards.keys_for_sex[0]} - Женский\n'
                         f'{keyboards.keys_for_sex[1]} - Мужской\n'
                         f'{keyboards.key_no_sex} - Не важно\n'
                         f'{keyboards.key_save_and_cancel[0]} - Сохранить ответы\n'
                         f'{keyboards.key_save_and_cancel[1]} - Вернуться назад', reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_get_sex_info.set()


async def choose_sex_info(message: types.Message):
    if message.text in keyboards.keys_for_sex or message.text in keyboards.key_no_sex:
        user.set_sex(message.text)
        await StageExtraRegistration.waiting_for_get_sex_info.set()

    elif message.text in keyboards.key_save_and_cancel:
        if message.text == keyboards.key_save_and_cancel[0]:
            db_users.save_sex_info(message.from_user.id, user.sex)

        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_zodiac_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(3):
        keyboard.row(keyboards.keys_zodiac[4 * i], keyboards.keys_zodiac[4 * i + 1],
                     keyboards.keys_zodiac[4 * i + 2], keyboards.keys_zodiac[4 * i + 3])
    keyboard.row(*keyboards.key_save_and_cancel)

    await message.answer('Выбери знак зодиака собеседника, которого хочешь найти:\n'
                         f'{keyboards.keys_zodiac[0]} - Овен\n'
                         f'{keyboards.keys_zodiac[1]} - Телец\n'
                         f'{keyboards.keys_zodiac[2]} - Близнецы\n'
                         f'{keyboards.keys_zodiac[3]} - Рак\n'
                         f'{keyboards.keys_zodiac[4]} - Лев\n'
                         f'{keyboards.keys_zodiac[5]} - Дева\n'
                         f'{keyboards.keys_zodiac[6]} - Весы\n'
                         f'{keyboards.keys_zodiac[7]} - Скорпион\n'
                         f'{keyboards.keys_zodiac[8]} - Стрелец\n'
                         f'{keyboards.keys_zodiac[9]} - Козерог\n'
                         f'{keyboards.keys_zodiac[10]} - Водолей\n'
                         f'{keyboards.keys_zodiac[11]} - Рыбы\n'
                         f'{keyboards.key_save_and_cancel[0]} - Сохранить ответы\n'
                         f'{keyboards.key_save_and_cancel[1]} - Вернуться назад', reply_markup=keyboard)
    await StageExtraRegistration.waiting_for_get_zodiac_info.set()


async def choose_zodiac_info(message: types.Message):
    if message.text in keyboards.keys_zodiac:
        if message.text not in user.zodiac:
            user.set_zodiac(message.text)

        await StageExtraRegistration.waiting_for_get_zodiac_info.set()

    elif message.text in keyboards.key_save_and_cancel:
        if message.text == keyboards.key_save_and_cancel[0]:
            db_users.save_zodiac_info(message.from_user.id, user.zodiac)

        await extra_registration(message)

    else:
        await message.answer("Пожалуйста, использйте клавиатуру ниже.")
        return


async def get_age_range_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.key_save_and_cancel)

    await message.answer('Напишите промежуток возраста, в котором вы хотите найти собеседника (два числа)',
                         reply_markup=keyboard)

    await StageExtraRegistration.waiting_for_get_age_range_info.set()


async def choose_age_range_info(message: types.Message):
    if not message.text.isdigit():
        if message.text in keyboards.key_save_and_cancel:
            if message.text == keyboards.key_save_and_cancel[0]:
                db_users.save_zodiac_info(message.from_user.id, user.zodiac)

            await extra_registration(message)
        else:
            await message.answer('Возраст должен быть цифрами, введите заново')
            return
    else:
        if user.age_range.__len__() != 2:
            user.set_age_range(message.text)
            await StageExtraRegistration.waiting_for_get_age_range_info.set()
        else:
            await message.answer('Два числа уже введены')
            return
