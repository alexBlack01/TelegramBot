import asyncio
import re
import extra_registration
import handlers
import keyboards
import config
import notifications
import registration
import db_users
import remove_user
import search_user

from emoji import emojize
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

greetings = [r'\b[П, п]р.в', r'[Х, х][а, э, е][ю, й]\D*', r'Даров?', r'\D*д.ров?',
             r'\D*дра\D*т?у?те', r'[К, к]у', r'[Й, й]оу', r'[Д, д]обрый день',
             r'[Д, д]оброе утро', r'[Д, д]обрый вечер', r'[П, п]ис', r'\D*[С, с]алам\D*']


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
    if db_users.check_user(message.from_user.id):
        await base_menu(message)
    else:
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
    keyboard.row(*keyboards.keys_for_resolution)

    await message.answer('Ты разрешаешь обработку персональных данных?', reply_markup=keyboard)
    await StageBot.waiting_for_choose_check_resolution.set()


async def choose_check_resolution(message: types.Message):
    if message.text not in keyboards.keys_for_resolution:
        await message.answer("Пожалуйста, выберите варинат, используя клавиатуру ниже.")
        return

    elif message.text == keyboards.keys_for_resolution[0]:
        db_users.check_and_add_user(message)

        await message.answer('Отлично!', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Итак, начнем.')

        db_users.set_state(message.from_user.id, config.S_REGISTRATION)
        await registration.registration(message)

    elif message.text == keyboards.keys_for_resolution[1]:
        await message.answer('Прости, но тогда я не смогу тебе помочь со знакомствами!')
        await message.answer('Ты разрешаешь обработку персональных данных?')
        return


async def base_menu(message: types.Message):
    loop = asyncio.get_event_loop()
    loop.create_task(notifications.long_wait(config.CONST_FOR_LONG_WAIT, message))

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboards.keys_base_menu)

    await message.answer(emojize('Меню:\n'
                                 f'{keyboards.keys_base_menu[0]} - Начать поиск\n'
                                 f'{keyboards.keys_base_menu[1]} - Выбрать поиск\n'
                                 f'{keyboards.keys_base_menu[2]} - Пройти дополнительную регистрацию\n'
                                 f'{keyboards.keys_base_menu[3]} - Удалить анкету\n', use_aliases=True),
                         reply_markup=keyboard)

    await StageBot.waiting_for_base_menu.set()


async def choose_base_menu(message: types.Message):
    if message.text == keyboards.keys_base_menu[0]:
        await search_user.regular_search(message)
    elif message.text == keyboards.keys_base_menu[2]:
        await extra_registration.extra_registration(message)
    elif message.text == keyboards.keys_base_menu[3]:
        await remove_user.remove_user(message)
    else:
        await message.answer('Остальные функции пока что не готовы!')
        return


async def main():
    bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    handlers.register_handlers_bot(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
