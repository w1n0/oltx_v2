import telebot
from telebot import types
bot = telebot.TeleBot("1441990058:AAGLBfOXwZV2LUFWuG2mwGzJYe8N5Zlw7zA")
import time

import pyowm
from pyowm import *
from pyowm.utils.config import get_default_config
configuration = get_default_config()
configuration['language'] = 'ru'
owm = OWM('e6910af1fedcad1885a807ec3a1b3a6f', configuration)



#Приветствие, появляется по команде и вызывает клавиатуру
@bot.message_handler(commands=['start'])
def send_welcome(message):
    stick_hello = open('s_hello.tgs', 'rb')
    bot.send_sticker(message.chat.id, stick_hello)
    stick_hello.close()
    bot.send_message(
        message.chat.id,
        '''Метеоцентр "Крылья по ветру" приветствует вас!

        Куда намечен ближайший вылет Совушки?
        ''',
        reply_markup=keyboard())

#Одноуровневая обработка комманд с клавиатуры
@bot.message_handler(content_types=["text"])
def send_anytext(message):    
    chat_id = message.chat.id

    if message.text == '☔ Питер, как всегда! ☔':

        sity = "Питер"
        weather_manager = owm.weather_manager()
        observation = weather_manager.weather_at_place(sity)
        detailed_status = observation.weather.detailed_status
        temp = observation.weather.temperature('celsius')['temp']

        weather = observation.weather
        status = weather.detailed_status

        bot.send_message (message.chat.id, "Ведется рассчет погодных условий")
        stick_calculate = open('s_calculate.tgs', 'rb')
        bot.send_sticker(message.chat.id, stick_calculate)
        stick_calculate.close()
        time.sleep(2)

        answer_1st = "Итак, сейчас в Питере ситуация следующая:" + "\n"
        bot.send_message (message.chat.id, answer_1st)

        answer_2nd = "Температура примерно " + str(temp)
        bot.send_message (message.chat.id, answer_2nd)

        answer_3rd = "В плане погоды - " + status + "\n\n"
        bot.send_message (message.chat.id, answer_3rd)

        if temp < 5.0:
            answer_4th = "Совушке крайне рекомендуется утеплить ушки!" + "\n"
            bot.send_message (message.chat.id, answer_4th)
        elif temp > 5.0:
            answer_4th = "Хорошая погода на дворе! Совушка может полетать вволю!" + "\n"
            bot.send_message (message.chat.id, answer_4th)

        stick_end = open('s_end.tgs', 'rb')
        bot.send_sticker(message.chat.id, stick_end,reply_markup=keyboard())
        stick_end.close()


        answer_bye =         '''Метеоцентр "Крылья по ветру" желает приятного полета,

        Будем рады видеть вас снова!
        '''
        bot.send_message(message.chat.id, answer_bye,parse_mode='HTML',reply_markup=keyboard())

    if message.text == '☀ В город потеплее! ☀':
        answer_bye = '''С грустью сообщаем, что в связи с короновирусом

        вылеты в теплые страны пока недоступны(
        '''
        stick_fail = open('s_fail.tgs', 'rb')
        bot.send_sticker(message.chat.id, stick_fail,reply_markup=keyboard())
        stick_fail.close()

        bot.send_message(message.chat.id, answer_bye,parse_mode='HTML',reply_markup=keyboard())

#Клавиатура
def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton('☔ Питер, как всегда! ☔')
    markup.add(btn1)    
    btn2 = types.KeyboardButton('☀ В город потеплее! ☀')
    markup.add(btn2)
    return markup  

#Способ обхода постоянных падений бота
while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e) 
        time.sleep(15)