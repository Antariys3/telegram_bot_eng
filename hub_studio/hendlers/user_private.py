from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold  # Italic, as_numbered_list и тд
from aiogram.utils.markdown import hbold

from hub_studio.filters.chat_types import ChatTypeFilter
from hub_studio.reply import delete_kb, test_kb, get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Привет, {hbold(message.from_user.first_name)}!")
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )
    # await message.answer(f"{message}")  # все данные объекта message
    # await message.reply(message.text)  # ответить на сообщение


# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command('menu'), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:", reply_markup=delete_kb)


@user_private_router.message(F.text.lower() == "о магазине")
@user_private_router.message(Command('about'))
async def menu_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_router.message(F.text.lower() == "доп функции")
@user_private_router.message(Command('additional functions'))
async def menu_cmd(message: types.Message):
    await message.answer("Еще есть", reply_markup=test_kb)


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Варианты оплаты:"),
        "Картой в боте",
        "При получении карта/кеш",
        "В заведении",
        marker='✅ '
    )
    await message.answer(text.as_html())


# Символ | значит or. Символ & значит and
# .contains("str") фильтр поиска выражения в слове
@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower().contains("варианты доставки")))
@user_private_router.message(Command('shipping'))
async def menu_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Само вынос (сейчас прибегу заберу)",
            "Покушаю у Вас (сейчас прибегу)",
            marker='✅ '
        ),
        as_marked_section(
            Bold("Нельзя:"),
            "Почта",
            "Голуби",
            marker='❌ '
        ),
        sep='\n----------------------\n'
    )
    await message.answer(text.as_html())


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"номер получен")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"локация получена")
    await message.answer(str(message.location))


# @user_private_router.message()
# async def echo(message: types.Message):
#     try:
#         text = message.text.lower()
#         if text in ["привет", "hello", "hi", "хай"]:
#             await message.answer("И тебе привет!")
#         elif text in ["пока", "до свидания", "bya", ]:
#             await message.answer("И тебе пока!")
#         else:
#             await message.send_copy(chat_id=message.chat.id)
#     except AttributeError:
#         await message.answer("Хорошая попытка! 😀")


# @user_private_router.message(F.photo)
# async def menu_photo(message: types.Message):
#     await message.answer("Это фото:")
