import os
import random

import telebot
from telebot import types

from working_with_db import create_connection, creating_new_user, add_word_to_db, get_all_words, get_today_words

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
WORDS = {}


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
        learning_words(callback.message, get_today_words)
    elif callback.data == "yesterday_words":
        bot.send_message(callback.message.chat.id, "Функция находится в разработке")
    elif callback.data == "all_words":
        learning_words(callback.message, get_all_words)


def add_english(message):
    global WORDS
    telegram_user_id = message.chat.id
    WORDS[telegram_user_id] = {}
    WORDS[telegram_user_id]["eng"] = message.text.strip().title()
    bot.send_message(message.chat.id, "Напишите слово на русском")
    bot.register_next_step_handler(message, add_rus)


def add_rus(message):
    global WORDS
    telegram_user_id = message.chat.id
    WORDS[telegram_user_id]["ru"] = message.text.strip().title()
    add_word_to_db(telegram_user_id, WORDS[telegram_user_id]["eng"], WORDS[telegram_user_id]["ru"])
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Добавить слова", callback_data="add")
    markup.row(btn_1)
    bot.send_message(message.chat.id, "Добавить еще слова?", reply_markup=markup)


def learning_words(message, get_the_words):
    global WORDS
    telegram_user_id = message.chat.id
    my_words = get_the_words(telegram_user_id)
    if my_words is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Добавить слова", callback_data="add"))
        bot.send_message(message.chat.id, "Вы еще не добавляли слова", reply_markup=markup)
        return

    if telegram_user_id in WORDS and "words" in WORDS[telegram_user_id]:
        list_words = WORDS[telegram_user_id]["words"].copy()
    else:
        WORDS[telegram_user_id] = {}
        WORDS[telegram_user_id]["words"] = my_words.copy()
        list_words = WORDS[telegram_user_id]["words"].copy()

    if not list_words:
        list_words = WORDS[telegram_user_id]["words"].copy()

    random_index = random.choice(range(len(list_words)))
    element = list_words.pop(random_index)

    lot = random.randint(1, 2)
    reverse_lot = 2 if lot == 1 else 1
    WORDS[telegram_user_id]["test_word"] = element[lot]
    bot.send_message(message.chat.id, f"Напишите перевод слова {element[reverse_lot]}")
    bot.register_next_step_handler(message, checking_translated_word)


def checking_translated_word(message):
    word = message.text.strip().title()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Следующее слово", callback_data="learn_words"))
    if word == WORDS[message.chat.id]["test_word"]:
        bot.send_message(message.chat.id, "Правильно! Продолжаем?", reply_markup=markup)
    else:

        bot.send_message(message.chat.id,
                         f"Правильный перевод {WORDS[message.chat.id]['test_word']}. Хотите продолжить?",
                         reply_markup=markup)


if __name__ == "__main__":
    bot.polling(none_stop=True)
