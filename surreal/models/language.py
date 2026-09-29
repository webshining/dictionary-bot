from ..base import Base, current_session


class Language(Base):
    _table = "language"

    value: str
    display: str

    @classmethod
    async def get_all(cls):
        session = current_session.get()
        return [cls.model_validate(l) for l in await session.query("SELECT * FROM language")]
