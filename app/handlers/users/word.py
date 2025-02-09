from io import BytesIO

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from edge_tts import Communicate

from app.keyboards import MenuKeyboard
from app.states import WordState
from database.models import User
from loader import _
from utils import translate_word

from ..routes import user_router as router
from .dictionaries import _get_dictionaries_data

data = "word"
pos_tags = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition or subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS": "List item marker",
    "MD": "Modal",
    "NN": "Noun, singular",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP": "Particle",
    "SYM": "Symbol",
    "TO": "Infinitival to",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund/present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
}


@router.message(MenuKeyboard("Add word"))
@router.message(Command("add_word"))
async def _word(message: Message, state: FSMContext):
    await message.answer(_("Enter word:"))
    await state.set_state(WordState.add)


@router.message(StateFilter(WordState.add, None), F.text)
async def _word_add_with_translate(message: Message, user: User, state: FSMContext):
    word = message.text
    translates, samples, expressions = await translate_word(word)

    await state.update_data(word=f"{word}-{translates[0]}")
    await state.set_state(None)

    text = f"<blockquote>{word}</blockquote>\n\n<b><i>Translates:</i></b>"
    for translate in translates:
        text += f"\n- {translate}"
    text += f"\n\n<b><i>Samples:</i></b>"
    for sample, pos in samples:
        text += f"\n- {sample}\n<b>[POS]:</b> {pos}\n"
    text += f"\n\n<b><i>Expressions:</i></b>"
    for ex, de in expressions:
        text += f"\n- {ex}\n<b>[Definition]:</b> {de}\n"
    markup = (await _get_dictionaries_data(user, "word"))[1]

    communicate = Communicate(word, "en-GB-RyanNeural")
    bytes_voice = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            bytes_voice.write(chunk["data"])
    bytes_voice.seek(0)
    voice = BufferedInputFile(bytes_voice.getvalue(), filename="voice.ogg")

    await message.answer_voice(caption=text, reply_markup=markup, voice=voice)
