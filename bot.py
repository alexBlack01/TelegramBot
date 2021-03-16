import telebot
from telebot import types

bot = telebot.TeleBot('1740841113:AAESpLnLF5v-23dVnhen5l6nhvvybIB8O0Y')

name = ''
surname = ''
age = 0
sex = ''
city = ''


@bot.message_handler(content_types=['text', 'picture'])
def start(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Привет! Меня зовут Meet&Greet. Я открою тебе мир новых знакомств."
                                               "Но чтобы начать начать, мне нужно узнать у тебя некоторое количество "
                                               "данных.")
        bot.send_message(message.from_user.id, "Итак, начнем!")
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши Привет')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
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
    name = message.text

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        print("Data save")  # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
        print("Data not save")  # переспрашиваем


bot.polling(none_stop=True, interval=0)