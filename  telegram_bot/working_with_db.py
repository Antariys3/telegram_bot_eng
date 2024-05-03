import datetime
import sqlite3


def create_connection():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Создаем таблицу users
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, id_telegram INTEGER,"
        " name VARCHAR(50))")

    # Создаем таблицу english с внешним ключом на таблицу users
    cur.execute(
        "CREATE TABLE IF NOT EXISTS english (id INTEGER PRIMARY KEY AUTOINCREMENT, eng VARCHAR(50), ru VARCHAR(50),"
        " date DATE DEFAULT CURRENT_DATE, rating INTEGER,"
        " user_id_telegram INTEGER, FOREIGN KEY (user_id_telegram) REFERENCES users(id_telegram))")

    # Создаем таблицу weather с внешним ключом на таблицу users
    cur.execute(
        "CREATE TABLE IF NOT EXISTS weather (id INTEGER PRIMARY KEY AUTOINCREMENT, city VARCHAR(50),"
        " temperature INTEGER, date DATE DEFAULT CURRENT_DATE,"
        " user_id_telegram INTEGER, FOREIGN KEY (user_id_telegram) REFERENCES users(id_telegram))")

    conn.commit()
    cur.close()
    conn.close()


def creating_new_user(message):
    telegram_user_id = message.from_user.id
    name = message.from_user.first_name

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id_telegram = ?", (telegram_user_id,))
    user = cur.fetchone()

    if user is None:
        cur.execute(
            "INSERT INTO users "
            "(id_telegram, name) VALUES (?, ?)", (telegram_user_id, name))
        conn.commit()

    cur.close()
    conn.close()


def add_word_to_db(id_telegram, eng, ru):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO english (eng, ru, rating, user_id_telegram) VALUES (?, ?, ?, ?)",
                (eng, ru, 3, id_telegram))

    conn.commit()

    cur.close()
    conn.close()


def get_all_words(telegram_user_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM english WHERE user_id_telegram = ?", (telegram_user_id,))

    words = cur.fetchall()
    cur.close()
    conn.close()
    return words


def get_today_words(telegram_user_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    today_date = str(datetime.date.today())

    cur.execute("SELECT * FROM english WHERE user_id_telegram = ? AND date = ?", (telegram_user_id, today_date))

    words = cur.fetchall()
    cur.close()
    conn.close()
    return words


def get_yesterday_words(telegram_user_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    cur.execute("SELECT * FROM english WHERE user_id_telegram = ? AND date = ?", (telegram_user_id, yesterday))

    words = cur.fetchall()
    cur.close()
    conn.close()
    return words
