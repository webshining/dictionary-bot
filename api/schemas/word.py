from .base import BaseModelResponse


class WordResponse(BaseModelResponse):
    id: int
    word: str
    translate: str


class WordRequest(BaseModelResponse):
    word: str = None
    translate: str = None
    know: bool = None
