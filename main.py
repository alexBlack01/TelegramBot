import telebot
from telebot import types
import config
import Registration
import re

bot = telebot.TeleBot(token=config.TOKEN)

greetings = [r'\b[П, п]р.в', r'[Х, х][а, э, е][ю, й]\D*', r'Даров?', r'\D*д.ров?',
             r'\D*дра\D*т?у?те', r'[К, к]у', r'[Й, й]оу', r'[Д, д]обрый день',
             r'[Д, д]оброе утро', r'[Д, д]обрый вечер', r'[П, п]ис', r'\D*[С, с]алам\D*']

def is_greeting(message):
    for i in greetings:
        if re.search(i, message):
            return True
    return False

@bot.message_handler(content_types = ['text'])
def start(message):
    if is_greeting(message.text):
        bot.send_message(message.from_user.id, "Привет! Меня зовут Meet&Greet. Я открою тебе мир новых знакомств."
                                               "Но чтобы начать, мне нужно узнать у тебя некоторое количество данных.")
        bot.send_message(message.from_user.id, "Однако я не могу обрабатывать твои данные без твоего согласия.")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_yes = types.KeyboardButton(text='Разрешаю')
        key_no = types.KeyboardButton(text='Запрещаю')
        keyboard.row(key_yes, key_no)

        bot.send_message(message.from_user.id, "Ты разрешаешь обработку персональных данных?", reply_markup=keyboard)
        bot.register_next_step_handler(message, check_resolution)

    else:
        bot.send_message(message.from_user.id, 'Напиши: Привет')

def check_resolution(message):
   if message.text == 'Разрешаю':
       bot.send_message(message.from_user.id, 'Отлично!')
       bot.send_message(message.from_user.id, "Итак, начнем!")
       bot.send_message(message.from_user.id, "Как тебя зовут?")
       bot.register_next_step_handler(message, Registration.get_name)
   elif message.text == 'Запрещаю':
       bot.send_message(message.from_user.id, 'Прости, но тогда я не смогу тебе помочь со знакомствами!')
       bot.send_message(message.from_user.id, "Ты разрешаешь обработку персональных данных?")
       bot.register_next_step_handler(message, check_resolution)


bot.polling(none_stop=True)

#@bot.callback_query_handler(func=lambda call: True)
#def callback_worker(call):
#    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
#        print("Data save")  # код сохранения данных, или их обработки
#        bot.send_message(call.message.chat.id, 'Запомню : )');
#    elif call.data == "no":
#        print("Data not save")  # переспрашиваем


