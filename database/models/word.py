from datetime import UTC, datetime, timedelta

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, case, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel
from .language import Language


class Word(BaseModel):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False, server_default="")
    translations: Mapped[list["Translation"]] = relationship(back_populates="word", lazy="joined", cascade="all, delete-orphan")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    repetitions: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    lapses: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    interval_days: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    ease_factor: Mapped[float] = mapped_column(Float, nullable=False, server_default="2.5")
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @classmethod
    async def get_study_cards(cls, user_id: int, limit: int, session):
        now = datetime.now(UTC)
        priority = case(
            (cls.due_at <= now, 0),
            (cls.due_at.is_(None), 1),
            else_=2,
        )
        statement = (
            select(cls)
            .where(cls.user_id == user_id)
            .order_by(priority, cls.due_at.asc().nullsfirst(), cls.lapses.desc(), cls.ease_factor.asc(), cls.id.asc())
            .limit(limit)
        )
        result = await session.execute(statement)
        return result.unique().scalars().all()

    def review(self, quality: int, now: datetime | None = None) -> None:
        if quality <= 0 or quality > 5:
            raise ValueError("quality must be between 0 and 5")

        now = now or datetime.now(UTC)
        if quality < 3:
            self.repetitions = 0
            self.lapses += 1
            self.interval_days = 1
        else:
            self.repetitions += 1
            if self.repetitions == 1:
                self.interval_days = 1
            elif self.repetitions == 2:
                self.interval_days = 6
            else:
                self.interval_days = max(1, round(self.interval_days * self.ease_factor))

        self.ease_factor = max(
            1.3,
            self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)),
        )
        self.last_reviewed_at = now
        self.due_at = now + timedelta(days=self.interval_days)


class Translation(BaseModel):
    __tablename__ = "user_word_translations"

    translation: Mapped[str] = mapped_column(String, nullable=False)

    word_id: Mapped[int] = mapped_column(ForeignKey("user_words.id"), primary_key=True)
    word: Mapped[Word] = relationship(back_populates="translations", lazy="select")

    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), primary_key=True)
    language: Mapped[Language] = relationship(lazy="joined")
