from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message

from database.models import User
from loader import _
from utils import translate_word

from ..routes import user_router as router
from .dictionaries import _get_dictionaries_data


@router.message(F.text)
async def _word_add_with_translate(message: Message, user: User, state: FSMContext):
    word = message.text
    translation = await translate_word(word, voice=True)
    translations = translation.translations
    examples = translation.examples
    expressions = translation.expressions
    voice = translation.voice

    await state.update_data(word=f"{word}-{translations[0]}")

    text = f"<blockquote>{word}</blockquote>\n\n<b><i>Translates:</i></b>"
    for translate in translations:
        text += f"\n- {translate}"
    text += f"\n\n<b><i>Examples:</i></b>"
    for ex in examples:
        text += f"\n- {ex.example}\n"
        if ex.position is not None:
            text += f"<b>[POS]:</b> {ex.position}\n"
    text += f"\n\n<b><i>Expressions:</i></b>"
    for ex in expressions:
        text += f"\n- {ex.expression}\n<b>[Definition]:</b> {ex.definition}\n"
    markup = (await _get_dictionaries_data(user, "word"))[1]

    await message.answer_voice(caption=text, reply_markup=markup, voice=BufferedInputFile(voice, filename="voice.ogg"))
