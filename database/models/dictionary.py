from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .word import Word
from ..base import BaseModel


class Dictionary(BaseModel):
    __tablename__ = "dictionaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    words: Mapped[list["Word"]] = relationship(lazy="select")
