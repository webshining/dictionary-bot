from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async

from bot.keyboards import DictionariesKeyboard, DictionaryKeyboard
from dictionary.models import Dictionary
from users.models import User
from ..routes import user_router as router
from ...text import Text


@router.message(Command("dictionaries"))
@router.message(F.text == Text.DICTIONARIES_BUTTON.value)
async def dictionaries_handler(message: Message, user: User):
    await message.delete()
    dictionaries = await sync_to_async(list)(user.dictionaries.all())
    await message.answer(str(Text.SELECT_DICTIONARY),
                         reply_markup=DictionariesKeyboard.keyboard("dictionaries", dictionaries))


@router.callback_query(DictionariesKeyboard.filter(F.data == "dictionaries"))
async def dictionaries_callback_handler(call: CallbackQuery, callback_data: DictionariesKeyboard):
    dictionary = await Dictionary.objects.aget(id=callback_data.id)
    await call.answer()
    await call.message.answer(f"<b>{dictionary.name}:</b>", reply_markup=DictionaryKeyboard.keyboard(dictionary.id))
