from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup


def weather_get():
    weather = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('Узнать погоду⛅')

    weather.add(button)
    return weather