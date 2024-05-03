from config import bot

# Импорт оставлен для других модулей, не удалять
from english_functions import english
from working_with_db import create_connection, creating_new_user


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name}")
    create_connection()
    creating_new_user(message)


@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Функция погоды в разработке")


if __name__ == "__main__":
    bot.polling(none_stop=True)
