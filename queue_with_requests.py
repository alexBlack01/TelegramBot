import asyncio

from aiogram import types

import db_users
import keyboards


async def work_with_queue(message: types.Message):
    while True:
        if db_users.check_queue(message.from_user.id):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(*keyboards.keys_for_resolution)

            await message.answer('Есть люди, которых хотят с тобой познакомиться!\n'
                                 'Хотел бы ты взгянуть?', reply_markup=keyboard)
