from datetime import datetime, timedelta, timezone

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .language import Language

user_language = Table(
    "user_language", BaseModel.metadata, Column("user_id", ForeignKey("users.id")), Column("language_id", ForeignKey("languages.id"))
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="user")
    lang: Mapped[str] = mapped_column(String, default="en")

    languages: Mapped[list["Language"]] = relationship(secondary=user_language, lazy="select")
    words: Mapped[list["Word"]] = relationship(back_populates="user", lazy="select")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user", lazy="select")


class Word(BaseModel):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="words")

    translations: Mapped[list["Translation"]] = relationship(back_populates="word", lazy="joined", cascade="all, delete-orphan")


class Translation(BaseModel):
    __tablename__ = "user_word_translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    translation: Mapped[str] = mapped_column(String, nullable=False)

    word_id: Mapped[int] = mapped_column(ForeignKey("user_words.id"))
    word: Mapped["Word"] = relationship(back_populates="translations", lazy="select")

    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    language: Mapped["Language"] = relationship(lazy="joined")


class Session(BaseModel):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    query_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    expired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(hours=1)
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions", lazy="select")

    def refresh(self):
        self.expired_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    def revoke(self):
        self.expired_at = datetime.now(timezone.utc)
