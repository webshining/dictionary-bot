from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from deep_translator import LingueeTranslator

from app.keyboards import MenuKeyboard
from app.states import WordState
from database.models import User
from loader import _

from ..routes import user_router as router
from .dictionaries import _get_dictionaries_data

data = "word"


@router.message(MenuKeyboard("Add word"))
@router.message(Command("add_word"))
async def _word(message: Message, state: FSMContext):
    await message.answer(_("Enter word:"))
    await state.set_state(WordState.add)


@router.message(WordState.add, F.text)
async def _word_add_with_translate(message: Message, user: User, state: FSMContext):
    translate = LingueeTranslator(source="auto", target="ru").translate(message.text)
    await state.update_data(word=f"{message.text}-{translate}")
    await state.set_state(None)
    text, markup = await _get_dictionaries_data(user, "word")
    await message.answer(text, reply_markup=markup)
