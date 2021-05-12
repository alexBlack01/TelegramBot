import asyncio

from aiogram import types


async def long_wait(wait_for, message: types.Message):
    while True:
        await asyncio.sleep(wait_for)

        await message.answer('Ты долго не заходил!')
