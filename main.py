import telebot
from telebot import types
import os

from english_functions import learning_words, add_english, add_rus
from working_with_db import create_connection, creating_new_user

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}")
    create_connection()
    creating_new_user(message)


@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Функция погоды в разработке")


@bot.message_handler(commands=["english"])
def english(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Добавить слова", callback_data="add")
    markup.row(btn_1)
    btn_2 = types.InlineKeyboardButton("Учить слова", callback_data="learn_words")
    btn_3 = types.InlineKeyboardButton("Повторить вчерашние слова", callback_data="yesterday_words")
    markup.row(btn_2, btn_3)
    btn_4 = types.InlineKeyboardButton("Повторить все слова", callback_data="all_words")
    markup.row(btn_4)
    bot.send_message(message.chat.id, "Выберите свой вариант", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == "add":
        bot.send_message(callback.message.chat.id, "Напишите слово на английском")
        bot.register_next_step_handler(callback.message, add_english)
    elif callback.data == "learn_words":
        learning_words(callback.message)
    elif callback.data == "yesterday_words":
        bot.send_message(callback.message.chat.id, "Функция находится в разработке")
    elif callback.data == "all_words":
        bot.send_message(callback.message.chat.id, "Функция находится в разработке")



if __name__ == "__main__":
    bot.polling(none_stop=True)
