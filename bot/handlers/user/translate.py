import re

from aiogram import F
from aiogram.types import Message, CallbackQuery
from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _

from ai.services import lemmatize
from bot.keyboards import DictionariesKeyboard, SaveKeyboard
from translations.services import translate
from users.models import User
from ..routes import user_router as router


@router.message(F.text, ~F.text.startswith("/"))
async def translate_handler(message: Message, user: User):
    words = list(filter(None, re.split(r"[ ,]+", message.text)))
    lemmatized = await lemmatize(words)

    dictionaries = await sync_to_async(list)(user.dictionaries.all())

    text = ""
    for l in lemmatized:
        text += f"\n<code>[</code>{l.strip()}<code>]</code>"

    await message.answer(
        text,
        reply_markup=DictionariesKeyboard.keyboard("translate", dictionaries),
        reply_to_message_id=message.message_id,
    )


@router.callback_query(DictionariesKeyboard.filter(F.data == "translate"))
async def translate_dictionary_handler(call: CallbackQuery, callback_data: DictionariesKeyboard, user: User):
    await call.answer()

    dictionary = await user.dictionaries.aget(id=callback_data.id)
    if not dictionary:
        await call.message.edit_text(_("Dictionary not found"), reply_markup=None)
        return

    words = re.findall(r"\[(\w+)\]", call.message.text)
    source_words = await translate(words, dictionary.source_lang)
    target_words = await translate(words, dictionary.target_lang)
    words = list(zip(source_words, target_words))

    text = ""
    for source_word, target_word in words:
        text += f"\n<code>[</code>{source_word}<code>]</code> — <code>[</code>{target_word}<code>]</code>"
    await call.message.edit_text(text, reply_markup=SaveKeyboard.keyboard(dictionary.id))


@router.callback_query(SaveKeyboard.filter())
async def translate_save_handler(call: CallbackQuery, callback_data: SaveKeyboard, user: User):
    await call.answer()

    dictionary = await user.dictionaries.aget(id=callback_data.id)
    if not dictionary:
        await call.message.edit_text(_("Dictionary not found"), reply_markup=None)
        return

    words = [list(pair) for pair in re.findall(r"\[(\w+)\] — \[(\w+)\]", call.message.text)]
    for word, translation in words:
        await dictionary.words.acreate(word=word, translation=translation)

    await call.message.edit_reply_markup(reply_markup=None)
