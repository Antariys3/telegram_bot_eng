import webbrowser

import telebot
from telebot import types

bot = telebot.TeleBot("foo")


@bot.message_handler(commands=["start", "main", "hello"])
def main(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name} {message.from_user.last_name}!",
    )
    # для передачи файлов использовать:
    # file = open(".static/passat.jpg", "rb")
    # bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Функция погоды в разработке")


@bot.message_handler(commands=["english"])
def english(message):
    bot.send_message(message.chat.id, "Изучение английского сейчас в разработке")


@bot.message_handler(content_types=["photo"])  # 'audio', 'video'
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    # markup.add(types.InlineKeyboardButton()) для добавления кнопки
    btn1 = types.InlineKeyboardButton("Перейти в Ютуб", url="https://youtube.com/")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton(
        "Удалить фото", callback_data="delete"
    )  # callback_data для передачи функции
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)
    bot.reply_to(
        message, "Какое красивое фото", reply_markup=markup
    )  # reply_markup передаём с сообщением еще и кнопки


# обработчик функций
@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text(
            "Текст изменён", callback.message.chat.id, callback.message.message_id
        )


@bot.message_handler(commands=["site", "website"])
def site(message):
    webbrowser.open("https://www.youtube.com/")


@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(
        message.chat.id, "<b>Информационная</b> <em>помощь!</em>", parse_mode="html"
    )


@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        # bot.send_message написать сообщение
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name} {message.from_user.last_name}!",
        )
    elif message.text.lower() == "id":
        # bot.reply_to ответ на сообщение
        bot.reply_to(message, f"ID {message.from_user.id}")


# Программа постоянно выполняется
bot.polling(none_stop=True)

