from .base import BaseModelResponse


class WordResponse(BaseModelResponse):
    id: int
    word: str
    translate: str
    known_count: int
    unknown_count: int


class WordProcessRequest(BaseModelResponse):
    know: bool


class WordRequest(BaseModelResponse):
    word: str
