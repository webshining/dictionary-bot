from datetime import UTC, datetime, timedelta

from pydantic import Field
from surrealdb import RecordID

from ..base import Base, current_session
from .language import Language
from .word import Word


class Know(Base):
    words: list[Word] = Field(default=[])

    repetitions: int = Field(default=0)
    lapses: int = Field(default=0)
    interval_days: int = Field(default=0)
    ease_factor: float = Field(default=2.5)
    due_at: datetime | None = Field(default=None)
    last_reviewed_at: datetime | None = Field(default=None)

    @classmethod
    async def get_study_cards(cls, user_id: RecordID, limit: int):
        session = current_session.get()

        query = """
        SELECT *,
        array::union([out.*], out->translation->word.*) as words,
        (IF due_at <= time::now() THEN 0 ELSE IF due_at = NONE THEN 1 ELSE 2 END) AS priority
        FROM know
        WHERE in = $user_id
        ORDER BY
            priority ASC,
            due_at ASC,
            lapses DESC,
            ease_factor ASC,
            id ASC
        LIMIT $limit
        FETCH words.language
        """

        return [cls.model_validate(c) for c in await session.query(query, {"user_id": user_id, "limit": limit})]

    async def review(self, quality: int, now: datetime | None = None) -> None:
        session = current_session.get()

        if quality <= 0 or quality > 5:
            raise ValueError("quality must be between 0 and 5")

        repetitions = 0
        lapses = 0
        interval_days = 0

        now = now or datetime.now(UTC)
        if quality < 3:
            repetitions = 0
            lapses = self.lapses + 1
            interval_days = 1
        else:
            repetitions = self.repetitions + 1
            if repetitions == 1:
                interval_days = 1
            elif repetitions == 2:
                interval_days = 6
            else:
                interval_days = max(1, round(interval_days * self.ease_factor))

        ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        last_reviewed_at = now
        due_at = now + timedelta(days=interval_days)

        await session.merge(
            self.id,
            {
                "repetitions": repetitions,
                "lapses": lapses,
                "interval_days": interval_days,
                "ease_factor": ease_factor,
                "last_reviewed_at": last_reviewed_at,
                "due_at": due_at,
            },
        )


class User(Base):
    name: str
    username: str | None = Field(default=None)
    lang: str = Field(default="en")
    status: str = Field(default="user")

    languages: list[Language] = Field(default=[])
    words: list[Know] = Field(default=[])

    async def _load_relation(self, name: str):
        session = current_session.get()

        if name == "languages":
            self.languages = [
                Language.model_validate(l) for l in await session.query(f"SELECT VALUE ->languages->language.* FROM ONLY {self.id}")
            ]
        elif name == "words":
            self.words = [
                Know.model_validate(w)
                for w in await session.query(
                    f"SELECT VALUE array::map(->know, |$know| {{id: $know.id, words: array::union([$know.out.*], $know.out->translation->word.*)}}) FROM ONLY {self.id} FETCH words.language"
                )
            ]

    @classmethod
    async def create_or_update(cls, id: int, **kwargs):
        session = current_session.get()

        response = await session.query(
            f"INSERT INTO user $data ON DUPLICATE KEY UPDATE {', '.join([f'{key} = $data.{key}' for key in kwargs])}",
            {"data": {**kwargs, "id": id}},
        )

        return cls.model_validate(response[0])

    async def toggle_language(self, id: str):
        session = current_session.get()

        if await session.query(f"record::exists(languages:{self.id.id}_{id})"):
            await session.delete(f"languages:{self.id.id}_{id}")
        else:
            await session.query(f"RELATE {self.id} ->languages:{self.id.id}_{id} ->language:{id}")

    async def change_lang(self, lang: str):
        session = current_session.get()

        self.lang = lang
        await session.merge(self.id, {"lang": lang})
