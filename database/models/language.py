from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import BaseModel


class Language(BaseModel):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
