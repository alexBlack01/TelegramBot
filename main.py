import telebot
from telebot import types
import config
import registration
import db_users

bot = telebot.TeleBot(token=config.TOKEN)

start_message = {
    u'Привет!\n'
    u'Меня зовут Meet&Greet.\n'
    u'Я открою тебе мир новых знакомств.\n'
    u'Но чтобы начать, мне нужно узнать у тебя некоторое количество данных.\n'
    u'Однако я не могу обрабатывать твои данные без твоего согласия.\n'
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_message)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes = types.KeyboardButton(text='Разрешаю')
    key_no = types.KeyboardButton(text='Запрещаю')
    keyboard.row(key_yes, key_no)

    bot.send_message(message.from_user.id, 'Ты разрешаешь обработку персональных данных?', reply_markup=keyboard)
    bot.register_next_step_handler(message, check_resolution)


def check_resolution(message):
    if message.text == 'Разрешаю':
        db_users.check_and_add_user(message)

        bot.send_message(message.from_user.id, 'Отлично!', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, 'Итак, начнем!')

        db_users.set_state(message.from_user.id, config.S_REGISTRATION)
        registration.registration(message)

    elif message.text == 'Запрещаю':
        bot.send_message(message.from_user.id, 'Прости, но тогда я не смогу тебе помочь со знакомствами!')
        bot.send_message(message.from_user.id, 'Ты разрешаешь обработку персональных данных?')
        bot.register_next_step_handler(message, check_resolution)


@bot.message_handler(func=lambda message: db_users.get_current_state(message.from_user.id) == config.S_MENU)
def base_menu(message):
    bot.send_message(message.from_user.id, 'Спасибо за регистрацию!')


bot.polling(none_stop=True)
