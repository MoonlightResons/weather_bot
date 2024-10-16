import telebot
import config
import sqlite3
from func import weather,changeinfo,send_info,new_user_register
from keyboard import weather_get


bot = telebot.TeleBot(config.TOKEN)

connection = sqlite3.connect('weather.db')
c = connection.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS Users (
          id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER UNIQUE NOT NULL,
          city TEXT)
          ''')


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Приветствую', reply_markup=weather_get())
    new_user_register(message.chat.id)


@bot.message_handler(func=lambda message: True)
def messages(message):
    if message.text == 'Узнать погоду⛅':
        bot.send_message(message.chat.id, 'Введите название города:')
        bot.register_next_step_handler(message, lambda message: weather(message, bot))

bot.polling()


