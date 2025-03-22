from io import BytesIO

import aiosqlite
import nltk
from edge_tts import Communicate
from googletrans import Translator
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from pydantic import BaseModel

from data.config import DIR

nltk.download("punkt_tab")
nltk.download("universal_tagset")
nltk.download("averaged_perceptron_tagger_eng")


class ExpressionModel(BaseModel):
    expression: str
    definition: str


class ExampleModel(BaseModel):
    position: str = None
    example: str


class Translation(BaseModel):
    voice: bytes | None = None
    translations: list[str] = []
    examples: list[ExampleModel] = []
    expressions: list[ExpressionModel] = []


async def translate_word(word: str, target: str = "ru", voice: bool = False) -> Translation:
    async with Translator() as translator:
        # translate
        translate = await translator.translate(word, dest=target)

        # voice
        bytes_voice = None
        if voice:
            communicate = Communicate(word, "en-GB-RyanNeural")
            bytes_voice = BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    bytes_voice.write(chunk["data"])
            bytes_voice.seek(0)
            bytes_voice = bytes_voice.getvalue()

        examples = await get_examples(word)
        return Translation(voice=bytes_voice, translations=[translate.text], examples=examples, expressions=[])


async def get_examples(word: str) -> list[ExampleModel]:
    examples = []
    query_word = f'"{word.strip()}"'
    async with aiosqlite.connect(DIR.joinpath("sentences.sqlite3")) as db:
        async with db.execute("SELECT content FROM sentences WHERE content MATCH ? LIMIT 20", (query_word,)) as cursor:
            async for row in cursor:
                tokens = word_tokenize(row[0])
                if len(tokens) > 28:
                    continue
                if " " not in word:
                    tags = pos_tag(tokens, tagset="universal")
                    for _word, tag in tags:
                        if _word == word:
                            examples.append(ExampleModel(position=tag, example=row[0]))
                            break
                else:
                    examples.append(ExampleModel(example=row[0]))
    return examples
