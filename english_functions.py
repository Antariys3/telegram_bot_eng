import os
import random

import telebot
from telebot import types

from working_with_db import get_the_words

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

WORDS = {}

