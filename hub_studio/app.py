import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from bot_cmds_list import private
from config import TELEGRAM_BOT_TOKEN
from database.engine import create_db, drop_db, session_maker
from hub_studio.hendlers.admin_private import admin_router
from hub_studio.hendlers.user_group import user_group_router
from hub_studio.hendlers.user_private import user_private_router
from hub_studio.middlewares.db import DataBaseSession

# Обновления, которые присылает API телеграмма
# ALLOWED_UPDATES = ['messages', 'edited_messages', 'callback_query']
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
# Создание списка админов. Введите /admin в группе, потом /admin в лс.
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)


async def on_startup(bot):
    # Функция создаёт все таблицы перед запуском бота и может удалить все таблицы
    # Для удаления в терминале написать python3 app.py run_param=True
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print("Сессия окончена!")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # await bot.delete_webhook(drop_pending_updates=True) # удаление всех ожидающих запросов
    await bot.set_my_commands(
        commands=private, scope=types.BotCommandScopeAllPrivateChats()
    )
    # удаление кнопки меню
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # resolve_used_update_types - использование всех апдейтов(сообщения, редак. сообщений, ответы от кнопок inline)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
