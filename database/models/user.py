from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .dictionary import Dictionary


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="user")
    lang: Mapped[str] = mapped_column(String, default="en")
    dictionaries: Mapped[list["Dictionary"]] = relationship(lazy="select", cascade="all, delete-orphan")

    async def get_dictionaries(self) -> list[Dictionary]:
        return await self.awaitable_attrs.dictionaries
