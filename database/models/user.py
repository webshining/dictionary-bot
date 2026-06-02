from sqlalchemy import BigInteger, Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .language import Language
from .word import Word

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
    words: Mapped[list[Word]] = relationship(lazy="select")
