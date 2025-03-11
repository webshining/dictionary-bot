from aiogram import F, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboards import DictionariesKeyboard, DictionaryKeyboard, MenuKeyboard
from app.states import DictionariesState, WordState
from database import AsyncSession
from database.models import Dictionary, User, Word
from loader import _

from ..routes import user_router as router


@router.message(MenuKeyboard("Dictionaries"))
@router.message(Command("dictionaries"))
async def _dictionaries(message: Message, user: User):
    text, markup = await _get_dictionaries_data(user, "dictionaries")

    await message.answer(text, reply_markup=markup)


@router.callback_query(DictionariesKeyboard.filter(F.data.in_(("word", "dictionaries"))))
async def _dictionaries_dictionary(
    call: CallbackQuery, user: User, session: AsyncSession, state: FSMContext, callback_data: DictionariesKeyboard
):
    await call.answer()
    if callback_data.action == "create":
        if callback_data.data == "word":
            await call.message.edit_reply_markup(reply_markup=None)
            await call.message.answer(_("Enter dictionary name:"))
            await state.set_state(WordState.dictionary_create)
            return
        await call.message.answer(_("Enter dictionary name:"))
        await state.set_state(DictionariesState.create)
    elif callback_data.action == "refresh":
        markup = (await _get_dictionaries_data(user, callback_data.data))[1]
        try:
            await call.message.edit_reply_markup(reply_markup=markup)
        except:
            pass
    elif callback_data.data == "dictionaries":
        dictionary = await Dictionary.get_by(id=callback_data.id, user_id=user.id, session=session)
        if not dictionary:
            return await _dictionaries(call.message, user, session, True)
        await call.message.answer(f"{dictionary.name}", reply_markup=DictionaryKeyboard.keyboard(id=dictionary.id))
    else:
        data = await state.get_data()
        word = [w.strip() for w in data.get("word").split("-") if w.strip()]
        await Word.create(dictionary_id=callback_data.id, word=word[0], translate=word[1], session=session)

        await call.answer(_("Word successfully added"))
        await call.message.edit_reply_markup(reply_markup=None)


@router.callback_query(DictionaryKeyboard.filter())
async def _dictionary(call: CallbackQuery, user: User, session: AsyncSession, callback_data: DictionaryKeyboard):
    if callback_data.action == "delete":
        await Dictionary.delete_by(id=callback_data.id, user_id=user.id, session=session)
        await call.message.edit_text(_("Dictionary successfully deleted."), reply_markup=None)


@router.message(StateFilter(DictionariesState.create, WordState.dictionary_create), F.text)
async def _dictionaries_create(message: Message, user: User, session: AsyncSession, state: FSMContext):
    dictionary = await Dictionary.create(name=message.text, user_id=user.id, session=session)
    await message.answer(_("Dictionary {} created successfully").format(html.quote(message.text)))

    if await state.get_state() == WordState.dictionary_create.state:
        data = await state.get_data()
        word = [w.strip() for w in data.get("word").split("-") if w.strip()]
        await Word.create(word=word[0], translate=word[1], dictionary_id=dictionary.id, session=session)
        await message.answer(_("Word {} added to {} successfully").format(html.quote(word[0]), html.quote(message.text)))

    await state.set_state(None)


async def _get_dictionaries_data(user: User, data: str):
    dictionaries = await user.get_dictionaries()
    text = _("Select dictionary:")
    markup = DictionariesKeyboard.keyboard(data=data, dictionaries=dictionaries)
    return text, markup
