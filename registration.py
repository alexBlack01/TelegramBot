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

def get_name(message):
    global name
    name = message.text
    user.id = message.from_user.id
    user.name = name
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Возраст должен быть цифрами')
        bot.register_next_step_handler(message, get_age)

    age = int(message.text)
    user.age = age
    bot.send_message(message.from_user.id, 'А какой у тебя пол?')
    bot.register_next_step_handler(message, get_sex)

def get_sex(message):
    global sex
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_male = types.InlineKeyboardButton(text='М', callback_data='male')  # кнопка «Да»
    keyboard.add(key_male)  # добавляем кнопку в клавиатуру
    key_female = types.InlineKeyboardButton(text='Ж', callback_data='female')
    keyboard.add(key_female)

    bot.send_message(message.from_user.id, 'А какой у тебя пол?')
    bot.register_next_step_handler(message, get_sex)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def get_city(message):
    global city
    city = message.text
    user.city = city

def add_user_in_db():
    db_users.check_and_add_user(user)