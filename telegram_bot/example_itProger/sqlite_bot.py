import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot("6611693232:AAGaMm60JUQLT49yn5RtHIS8aw7t5nLKcLM")
name = ""


@bot.message_handler(commands=["start"])
def start(message):
    conn = sqlite3.connect("../database.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), password varchar(50))"
    )
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(
        message.chat.id, "Привет, мы тебя сейчас зарегистрируем. Введите имя"
    )
    # Функция, которая будет вызываться после отправки сообщение
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect("../database.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO user(name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Список пользователей", callback_data="user"))
    bot.send_message(
        message.chat.id, "Пользователь зарегистрирован!", reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    conn = sqlite3.connect("../database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    info = ""
    for user in users:
        info += f"Имя: {user[1]}, Пароль: {user[2]}\n"
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)
