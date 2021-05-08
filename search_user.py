import random
import db_users

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class StageSearch(StatesGroup):
    waiting_for_regular_search = State()


async def regular_search(message: types.Message):
    users = db_users.get_all_users()
    user = random.choice(users)

    await message.answer('Меня зовут <b>Meet&Greet</b>.\n\n'
                         'Я открою тебе мир новых знакомств.\n'
                         'Но чтобы начать, мне нужно узнать у тебя некоторое количество данных.\n'
                         'Однако я не могу обрабатывать твои данные без твоего согласия.')


    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                         caption=emojize(caption),
                         reply_to_message_id=message.message_id)
    await StageSearch.waiting_for_regular_search.set()

async def regular_search_choose():
