import logging
import telebot
from telebot import types
import config
import db_users
import user

bot = telebot.TeleBot(token=config.TOKEN)

user = user.User()


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_REGISTRATION)
def registration(message):
    user.set_id(message.from_user.id)

    bot.send_message(message.from_user.id, 'Как тебя зовут?')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text
    user.set_name(name)

    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    age = message.text
    if not age.isdigit():
        bot.send_message(message.from_user.id, 'Возраст должен быть цифрами')
        bot.register_next_step_handler(message, get_age)
        return

    age = int(age)
    user.set_age(age)

    bot.register_next_step_handler(message, get_sex)


def get_sex(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_man = types.KeyboardButton(text='М')
    key_woman = types.KeyboardButton(text='Ж')
    keyboard.row(key_man, key_woman)

    bot.send_message(message.from_user.id, 'А какой у тебя пол?', reply_markup=keyboard)

    sex = message.text
    user.set_sex(sex)

    bot.send_message(message.from_user.id, 'А в каком городе ты находишься?', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_city)


def get_city(message):
    types.ReplyKeyboardRemove()
    city = message.text
    user.set_city(city)

    bot.send_message(message.from_user.id, 'Отсалось только загрузить фото')
    bot.register_next_step_handler(message, get_photo)


@bot.message_handler(content_types=['document'])
def get_photo(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:\\Users\\asfsa\\Repository\\PI\\TelegramBot\\photos\\' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    user.set_photo(src)

    db_users.save_user_form(user)
    db_users.set_state(user.id, config.S_MENU)
