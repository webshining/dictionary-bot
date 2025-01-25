from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import BaseModel


class Word(BaseModel):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("dictionaries.id"))
