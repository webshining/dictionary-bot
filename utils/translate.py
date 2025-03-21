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
    voice: bytes | None = None
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


from googletrans import Translator


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

        return Translation(voice=bytes_voice, translations=[translate.text], examples=[], expressions=[])
