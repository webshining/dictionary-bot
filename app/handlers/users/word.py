from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from deep_translator import GoogleTranslator, LingueeTranslator
from textblob import TextBlob

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
    word = str(TextBlob(message.text).correct())
    try:
        translates = LingueeTranslator(source="english", target="russian").translate(word, return_all=True)[:4]
    except:
        pass
    translates = [GoogleTranslator(source="english", target="ru").translate(word)]

    await state.update_data(word=f"{message.text}-{translates[0]}")
    await state.set_state(None)

    text = f"<blockquote>{word}</blockquote>"
    for translate in translates:
        text += f"\n- <i>{translate}</i>"

    markup = (await _get_dictionaries_data(user, "word"))[1]
    await message.answer(text, reply_markup=markup)
