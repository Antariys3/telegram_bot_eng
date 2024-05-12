from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from my_aiogram.kbrd import get_keyboard, delete_kb

english_router = Router()


class AddWords(StatesGroup):
    english = State()
    russian = State()


@english_router.message(CommandStart())
async def start_com(massage: types.Message):
    await massage.answer(f"Привет {massage.chat.first_name}!")


@english_router.message((F.text.lower() == "eng") | (F.text.lower() == "анг"))
@english_router.message(Command("english"))
async def english(massage: types.Message):
    await massage.answer(
        "Я помогу тебе с изучением иностранного языка",
        reply_markup=get_keyboard(
            "Добавить слова",
            "Учить сегодняшние слова",
            "Повторить вчерашние слова",
            "Повторить все слова",
            placeholder="Выберете свой вариант",
            sizes=(2, 2)
        ))


@english_router.message(StateFilter(None), F.text.lower() == "добавить слова")
async def add_words(massage: types.Message, state: FSMContext):
    await massage.answer("Введите иностранное слово", reply_markup=delete_kb)
    await state.set_state(AddWords.english)


@english_router.message(AddWords.english, F.text)
async def add_eng_word(massage: types.Message, state: FSMContext):
    await state.update_data(english=massage.text)
    await massage.answer("Введите русское слово")
    await state.set_state(AddWords.russian)


@english_router.message(AddWords.russian, F.text)
async def add_rus_word(massage: types.Message, state: FSMContext):
    await state.update_data(russian=massage.text)
    await massage.answer("Слова добавлены")
    data = await state.get_data()
    await massage.answer(str(data))
    await state.clear()


@english_router.message(F.text.lower() == "учить сегодняшние слова")
async def learn_today_words(massage: types.Message):
    await massage.answer("Учим сегодняшние слова", reply_markup=delete_kb)


@english_router.message(F.text.lower() == "повторить вчерашние слова")
async def repeat_yesterday_words(massage: types.Message):
    await massage.answer("Повторяем вчерашние слова", reply_markup=delete_kb)


@english_router.message(F.text.lower() == "повторить все слова")
async def repeat_all_words(massage: types.Message):
    await massage.answer("Повторяем все слова", reply_markup=delete_kb)
