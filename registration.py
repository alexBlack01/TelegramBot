import telebot
from telebot import types
import config
import db_users
import user

bot = telebot.TeleBot(token=config.TOKEN)

user = user.User()

name = ''
surname = ''
age = 0
sex = ''
city = ''
photo = ''

@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_NAME)
def get_name(message):
    global name
    name = message.text
    user.id = message.from_user.id
    user.name = name
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_AGE)
def get_age(message):
    global age
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Возраст должен быть цифрами')
        bot.register_next_step_handler(message, get_age)

    age = int(message.text)
    user.age = age
    bot.register_next_step_handler(message, get_sex)

@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_SEX)
def get_sex(message):
    global sex
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_man = types.KeyboardButton(text='М')
    key_woman = types.KeyboardButton(text='Ж')
    keyboard.row(key_man, key_woman)

    bot.send_message(message.from_user.id, "А какой у тебя пол?", reply_markup=keyboard)

    sex = message.text
    user.sex = sex
    bot.send_message(message.from_user.id, 'А в каком городе ты находишься?')
    bot.register_next_step_handler(message, get_city)

@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_CITY)
def get_city(message):
    global city
    city = message.text
    user.city = city

    bot.register_next_step_handler(message, add_user_in_db)

@bot.message_handler(content_types=['document'], func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_GET_PHOTO)
def get_photo(message):

    global photo
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'C:/Python/Project/tg_bot/files/received/' + message.document.file_name;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


def add_user_in_db(message):
    db_users.check_and_add_user(user)
    bot.send_message(message.from_user.id, 'Спасибо за регистрацию!')