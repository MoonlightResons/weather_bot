import requests
import sqlite3
import threading

conn = sqlite3.connect('weather.db', check_same_thread=False)
local = threading.local()
db_lock = threading.Lock()


def get_db_connection():
    if not hasattr(local, "connection"):
        local.connection = sqlite3.connect('weather.db')
    return local.connection


def changeinfo(user_id: str, name, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"UPDATE Users SET {name} = ? WHERE user_id = ?", (info, user_id))
        connection.commit()


def send_info(user_id: str, info):
    connection = get_db_connection()
    with connection:
        c = connection.cursor()
        c.execute(f"SELECT {info} FROM Users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0]
    

def get_user_id(user_id: int):
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM Users WHERE user_id = ?', (user_id,))
    return cursor.fetchone() is not None


def new_user_register(user_id: int):
    cursor = conn.cursor()
    if not get_user_id(user_id):
        cursor.execute('INSERT INTO Users (user_id) VALUES (?)', (user_id,))
        conn.commit()
    else:
        pass


def weather(message, bot):
    user_message = message.text
    changeinfo(message.chat.id, 'city', user_message)
    city = send_info(message.chat.id, 'city')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    
    weather_data = requests.get(url).json()

    if 'main' not in weather_data:
        bot.send_message(message.chat.id, f'Город "{city}" не найден. Пожалуйста, проверьте правильность написания.')
        return

    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])

    wind_speed = round(weather_data['wind']['speed'])

    weather_description = weather_data['weather'][0]['description']

    bot.send_message(
        message.chat.id,
        f'Сейчас в городе {city}: {temperature} °C\nОщущается как {temperature_feels} °C\nПогода: {weather_description}\nСкорость ветра: {wind_speed} м/с'
    )