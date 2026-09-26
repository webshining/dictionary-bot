from pydantic import BaseModel, Field

from .languages import Response as LanguageResponse


class Request(BaseModel):
    init_data: str


class TranslationResponse(BaseModel):
    translation: str
    language: LanguageResponse


class Response(BaseModel):
    id: int
    source: str
    translations: list[TranslationResponse]


class ReviewRequest(BaseModel):
    quality: int = Field(ge=0, le=5)
