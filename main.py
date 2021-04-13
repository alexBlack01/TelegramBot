import asyncio
import logging
import re
from typing import Set

from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand

import config
import registration
import db_users

logger = logging.getLogger(__name__)

greetings = [r'\b[П, п]р.в', r'[Х, х][а, э, е][ю, й]\D*', r'Даров?', r'\D*д.ров?',
             r'\D*дра\D*т?у?те', r'[К, к]у', r'[Й, й]оу', r'[Д, д]обрый день',
             r'[Д, д]оброе утро', r'[Д, д]обрый вечер', r'[П, п]ис', r'\D*[С, с]алам\D*']

keys_for_resolution = ['Разрешаю', 'Запрещаю']


class StageBot(StatesGroup):
    waiting_for_hello = State()
    waiting_for_check_hello = State()
    waiting_for_check_resolution = State()
    waiting_for_choose_check_resolution = State()
    waiting_for_registration = State()
    waiting_for_base_menu = State()


def is_greeting(message) -> bool:
    for i in greetings:
        if re.search(i, message):
            return True
    return False


async def say_hello(message: types.Message):
    await message.answer('Привет!')
    await StageBot.waiting_for_check_hello.set()


async def check_hello(message: types.Message):
    if is_greeting(message.text):
        await message.answer('Меня зовут <b>Meet&Greet</b>.\n\n'
                             'Я открою тебе мир новых знакомств.\n'
                             'Но чтобы начать, мне нужно узнать у тебя некоторое количество данных.\n'
                             'Однако я не могу обрабатывать твои данные без твоего согласия.')
        await check_resolution(message)
    else:
        await message.answer('Напиши: "Привет"')
        return


async def check_resolution(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*keys_for_resolution)

    await message.answer('Ты разрешаешь обработку персональных данных?', reply_markup=keyboard)
    await StageBot.waiting_for_choose_check_resolution.set()


async def choose_check_resolution(message: types.Message):
    if message.text not in keys_for_resolution:
        await message.answer("Пожалуйста, выберите варинат, используя клавиатуру ниже.")
        return

    elif message.text == 'Разрешаю':
        db_users.check_and_add_user(message)

        await message.answer('Отлично!', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Итак, начнем.')

        db_users.set_state(message.from_user.id, config.S_REGISTRATION)
        await registration.registration(message)

    elif message.text == 'Запрещаю':
        await message.answer('Прости, но тогда я не смогу тебе помочь со знакомствами!')
        await message.answer('Ты разрешаешь обработку персональных данных?')
        return


async def base_menu(message: types.Message):
    await message.answer('Основное меню')


def register_handlers_bot(dp: Dispatcher):
    dp.register_message_handler(say_hello, commands='start', state='*')
    dp.register_message_handler(check_hello, state=StageBot.waiting_for_check_hello)
    dp.register_message_handler(check_resolution, state=StageBot.waiting_for_check_resolution)
    dp.register_message_handler(choose_check_resolution, state=StageBot.waiting_for_choose_check_resolution)
    dp.register_message_handler(registration.registration,
                                state=registration.StageRegistration.waiting_for_registration)
    dp.register_message_handler(registration.get_name, state=registration.StageRegistration.waiting_for_name)
    dp.register_message_handler(registration.get_age, state=registration.StageRegistration.waiting_for_age)
    dp.register_message_handler(registration.get_sex, state=registration.StageRegistration.waiting_for_sex)
    dp.register_message_handler(registration.sex_chosen, state=registration.StageRegistration.waiting_for_sex_chosen)
    dp.register_message_handler(registration.get_city, state=registration.StageRegistration.waiting_for_city)
    dp.register_message_handler(registration.get_photo, state=registration.StageRegistration.waiting_for_photo,
                                content_types=[types.ContentType.PHOTO])
    dp.register_message_handler(base_menu, state=StageBot.waiting_for_base_menu)


async def main():
    bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_bot(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
