from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .word import Word


class Dictionary(BaseModel):
    __tablename__ = "dictionaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    words: Mapped[list["Word"]] = relationship(lazy="select", cascade="all, delete-orphan")

    async def get_words(self) -> list[Word]:
        return await self.awaitable_attrs.words
