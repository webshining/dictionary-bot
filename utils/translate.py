import sqlite3
from io import BytesIO

import aiosqlite
import nltk
from edge_tts import Communicate
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from data.config import DIR

nltk.download("punkt_tab")
nltk.download("universal_tagset")
nltk.download("averaged_perceptron_tagger_eng")

model_name = "Helsinki-NLP/opus-mt-en-ru"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


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


def translate(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


async def translate_word(word: str, target: str = "ru", voice: bool = False) -> Translation:
    translations = [translate(word)]

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
    return Translation(voice=bytes_voice, translations=translations, examples=examples, expressions=[])


conn = sqlite3.connect("sentences.sqlite3")


async def get_examples(word: str) -> list[ExampleModel]:
    examples = []
    query_word = f'"{word.strip()}"'  # Убираем лишние пробелы вокруг слова
    async with aiosqlite.connect(DIR.joinpath("sentences.sqlite3")) as db:
        async with db.execute(
            """
            SELECT full_content FROM sentences WHERE full_content MATCH ? 
            UNION ALL
            SELECT part_1 FROM sentences WHERE part_1 MATCH ? 
            UNION ALL
            SELECT part_2 FROM sentences WHERE part_2 MATCH ? 
            LIMIT 100
            """,
            (query_word, query_word, query_word),
        ) as cursor:
            sentences = [c[0] async for c in cursor]
            smallest_sentences = sorted(sentences, key=len)[:5]
            for sentence in smallest_sentences:
                if " " not in word:
                    tokens = word_tokenize(sentence)
                    tags = pos_tag(tokens, tagset="universal")
                    for _word, tag in tags:
                        if _word == word:
                            examples.append(
                                ExampleModel(example=sentence.replace(word, f"<code>{word}</code>"), position=tag)
                            )
                            break
                else:
                    examples.append(ExampleModel(example=sentence.replace(word, f"<code>{word}</code>")))

    return examples
