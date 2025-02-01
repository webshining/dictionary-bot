from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboards import DictionariesKeyboard, DictionaryKeyboard, MenuKeyboard
from app.states import DictionariesState
from database import AsyncSession
from database.models import Dictionary, User
from loader import _

from ..routes import user_router as router

data = "dictionaries"


@router.message(MenuKeyboard("Dictionaries"))
@router.message(Command("dictionaries"))
async def _dictionaries(message: Message, user: User, edit: bool = False):
    text, markup = await _get_dictionaries_data(user)

    if edit:
        return await message.edit_text(text, reply_markup=markup)
    await message.answer(text, reply_markup=markup)


@router.callback_query(DictionariesKeyboard.filter(F.data == data))
async def _dictionaries_dictionary(
    call: CallbackQuery, user: User, session: AsyncSession, state: FSMContext, callback_data: DictionariesKeyboard
):
    await call.answer()
    if callback_data.action == "create":
        await call.message.answer(_("Enter dictionary name:"))
        await state.set_state(DictionariesState.create)
    elif callback_data.action == "refresh":
        text, markup = await _get_dictionaries_data(user)
        try:
            await call.message.edit_text(text, reply_markup=markup)
        except:
            pass
    else:
        dictionary = await Dictionary.get_by(id=callback_data.id, user_id=user.id, session=session)
        if not dictionary:
            return await _dictionaries(call.message, user, session, True)
        await call.message.answer(f"{dictionary.name}", reply_markup=DictionaryKeyboard.keyboard(id=dictionary.id))


@router.callback_query(DictionaryKeyboard.filter())
async def _dictionary(call: CallbackQuery, user: User, session: AsyncSession, callback_data: DictionaryKeyboard):
    if callback_data.action == "delete":
        await Dictionary.delete_by(id=callback_data.id, user_id=user.id, session=session)
        await call.message.edit_text(_("Dictionary successfully deleted."), reply_markup=None)


@router.message(DictionariesState.create, F.text)
async def _dictionaries_create(message: Message, user: User, session: AsyncSession, state: FSMContext):
    dictionary = await Dictionary.create(name=message.text, user_id=user.id, session=session)

    await message.answer(_("Dictionary {} created successfully").format(html.quote(message.text)))
    await state.set_state(None)
    return dictionary


async def _get_dictionaries_data(user: User):
    dictionaries = await user.get_dictionaries()
    text = _("Select dictionary:")
    markup = DictionariesKeyboard.keyboard(data=data, dictionaries=dictionaries)
    return text, markup
