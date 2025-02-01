from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from deep_translator import GoogleTranslator

from app.keyboards import DictionariesKeyboard, MenuKeyboard
from app.states import WordState
from database import AsyncSession
from database.models import User, Word
from loader import _

from ..routes import user_router as router


@router.message(MenuKeyboard("Add word"))
@router.message(Command("add_word"))
async def _word(message: Message, state: FSMContext):
    await message.answer(_("Enter word:"))
    await state.set_state(WordState.add)


@router.message(WordState.add, F.text)
async def _word_add_with_translate(message: Message, user: User, state: FSMContext):
    translate = GoogleTranslator(source="auto", target="ru").translate(message.text)
    await state.update_data(word=f"{message.text}-{translate}")
    await state.set_state(None)
    text, markup = await _get_dictionaries_data(user, "word")
    await message.answer(text, reply_markup=markup)


@router.message(F.text.regexp(r"\s*\w+\s*-\s*\w+\s*"))
async def _word_add(message: Message, user: User, state: FSMContext):
    words = [w.strip() for w in message.text.split("-") if w.strip()]
    if len(words) != 2:
        return

    text, markup = await _get_dictionaries_data(user, "word")
    await message.answer(text, reply_markup=markup)
    await state.update_data(word=message.text)


@router.callback_query(DictionariesKeyboard.filter(F.data == "word"))
async def _word_dictionary(
    call: CallbackQuery, user: User, session: AsyncSession, state: FSMContext, callback_data: DictionariesKeyboard
):
    await call.answer()
    if callback_data.action in ("refresh", "create"):
        await _dictionaries_dictionary(call, user, session, state, callback_data)
    else:
        word = [w.strip() for w in (await state.get_data()).get("word").split("-") if w.strip()]
        await Word.create(dictionary_id=callback_data.id, word=word[0], translate=word[1], session=session)

        await call.message.edit_text(text=_("Word successfully added"), reply_markup=None)


@router.message(WordState.dictionary_create, F.text)
async def _word_dictionary_create(message: Message, user: User, session: AsyncSession, state: FSMContext):
    dictionary = await _dictionaries_create(message, user, session, state)
    word = [w.strip() for w in (await state.get_data()).get("word").split("-") if w.strip()]
    await Word.create(dictionary_id=dictionary.id, word=word[0], translate=word[1], session=session)
    await message.answer(_("Word successfully added"))
