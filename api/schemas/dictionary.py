from .base import BaseModelResponse
from .word import WordResponse


class DictionaryResponse(BaseModelResponse):
    id: int
    name: str
    words: list[WordResponse]


class DictionaryRequest(BaseModelResponse):
    name: str
