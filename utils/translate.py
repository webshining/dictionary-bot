from io import BytesIO

import aiohttp
from edge_tts import Communicate
from fake_useragent import UserAgent
from pydantic import BaseModel

ua = UserAgent()


class ExpressionModel(BaseModel):
    expression: str
    definition: str


class ExampleModel(BaseModel):
    position: str
    example: str


class Translation(BaseModel):
    voice: bytes
    translations: list[str] = []
    examples: list[ExampleModel] = []
    expressions: list[ExpressionModel] = []


def get_expressions(data: list):
    for d in data:
        yield ExpressionModel(expression=d["expression"], definition=d["def"])


def get_examples(data: list):
    for d in data:
        if d["Defs"]:
            if d["Defs"][0]["examples"]:
                yield ExampleModel(position=d["Pos"], example=d["Defs"][0]["examples"][0]["example"])


async def translate_word(word: str, target: str = "ru") -> Translation:
    async with aiohttp.ClientSession(headers={"User-Agent": ua.random}) as session:
        async with session.post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "format": "text",
                "from": "eng",
                "to": target,
                "input": word,
                "options": {
                    "sentenceSplitter": True,
                    "origin": "translation.web",
                    "contextResults": True,
                    "languageDetection": True,
                },
            },
        ) as response:
            data = await response.json()
            data = data["contextResults"]["results"][:3]
            translations = [d["translation"] for d in data]

        async with session.get(
            f"https://definition-api.reverso.net/v1/api/definitions/en/{word}?targetLang={target}&maxExpressions=60&showNeighbors=2&expressionDefs=6&wordExpressions=true&synonyms=false"
        ) as response:
            data = await response.json()
            data = data["DefsByWord"][0]
            examples = list(get_examples(data["DefsByPos"]))
            expressions = list(get_expressions(data["expressionDefs"]))

        communicate = Communicate(word, "en-GB-RyanNeural")
        bytes_voice = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                bytes_voice.write(chunk["data"])
        bytes_voice.seek(0)

        return Translation(
            voice=bytes_voice.getvalue(), translations=translations, examples=examples, expressions=expressions
        )
