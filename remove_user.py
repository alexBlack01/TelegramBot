import db_users
import keyboards
import main

from emoji import emojize
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State


class StageRemove(StatesGroup):
    waiting_for_remove = State()


async def remove_user(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*keyboards.keys_for_resolution)

    await message.answer('Ты уверен, что хочешь удалить анкету?', reply_markup=keyboard)
    await StageRemove.waiting_for_remove.set()


async def choose_remove_user(message: types.Message):
    if message.text not in keyboards.keys_for_resolution:
        await message.answer("Пожалуйста, выберите варинат, используя клавиатуру ниже.")
        return

    elif message.text == keyboards.keys_for_resolution[0]:
        db_users.delete_user(message.from_user.id)

        await message.answer('Прощай. Я буду по тебе скучать!', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(emojize(':sob:', use_aliases=True))

    elif message.text == keyboards.keys_for_resolution[1]:
        await message.answer(emojize('Фух, напугал! :scream_cat:', use_aliases=True))
        await main.base_menu(message)
