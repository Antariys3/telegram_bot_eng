import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from config import TELEGRAM_BOT_TOKEN
from my_aiogram.commands.bot_cmnd_list import menu
from my_aiogram.hendlers.english import english_router
from my_aiogram.hendlers.weather import weather_router

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()

dp.include_router(english_router)
dp.include_router(weather_router)


async def main():
    await bot.set_my_commands(commands=menu, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


asyncio.run(main())
