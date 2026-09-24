import asyncio

from database.base import get_session
from database.models import Word


async def main():
    async with get_session() as session:
        async with session.begin():
            for word in await Word.get_all(session=session):
                word.source = word.translations[0].translation
                await session.flush()


if __name__ == "__main__":
    asyncio.run(main())
