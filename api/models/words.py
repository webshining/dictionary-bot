from pydantic import BaseModel

from .languages import Response as LanguageResponse


class Request(BaseModel):
    init_data: str


class TranslationResponse(BaseModel):
    translation: str
    language: LanguageResponse


class Response(BaseModel):
    id: int
    translations: list[TranslationResponse]
