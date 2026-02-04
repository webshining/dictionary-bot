from pydantic import BaseModel

from .languages import Response as LanguageResponse


class Request(BaseModel):
    init_data: str


class Response(BaseModel):
    id: int
    name: str
    username: str
    lang: str
    languages: list[LanguageResponse]


