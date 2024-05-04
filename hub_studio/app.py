import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from config import TELEGRAM_BOT_TOKEN
from bot_cmds_list import private
from hub_studio.hendlers.user_private import user_private_router
from hub_studio.hendlers.user_group import user_group_router
from hub_studio.hendlers.admin_private import admin_router

# Обновления, которые присылает API телеграмма
ALLOWED_UPDATES = ['messages', 'edited_messages']
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
# Создание списка админов. Введите /admin в группе, потом /admin в лс.
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


async def main():
    # await bot.delete_webhook(drop_pending_updates=True) # удаление всех ожидающих запросов
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # удаление кнопки меню
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
