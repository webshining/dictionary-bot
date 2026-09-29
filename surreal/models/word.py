from surrealdb import RecordID

from ..base import Base
from .language import Language


class Word(Base):
    word: str
    language: RecordID | Language
