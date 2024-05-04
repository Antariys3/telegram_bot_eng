from aiogram import types, Router
from aiogram.filters import Command

weather_router = Router()


@weather_router.message(Command("weather"))
async def weather(message: types.Message):
    await message.answer("Функция погоды сейчас в разработке")
