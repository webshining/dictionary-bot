from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .language import Language


class Word(BaseModel):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    translations: Mapped[list["Translation"]] = relationship(back_populates="word", lazy="joined", cascade="all, delete-orphan")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Translation(BaseModel):
    __tablename__ = "user_word_translations"

    translation: Mapped[str] = mapped_column(String, nullable=False)

    word_id: Mapped[int] = mapped_column(ForeignKey("user_words.id"), primary_key=True)
    word: Mapped[Word] = relationship(back_populates="translations", lazy="select")

    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), primary_key=True)
    language: Mapped[Language] = relationship(lazy="joined")
