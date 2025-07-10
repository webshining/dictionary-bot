from pydantic import BaseModel


class LemmatizeResponse(BaseModel):
    words: list[str]


class TranslateResponse(BaseModel):
    synonyms: list[str]
    examples: list[str]
