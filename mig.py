import asyncio

from database.base import get_session
from database.models import Language, User, Word
from surreal.base import database
from surreal.models import Language as SLLanguage
from surreal.models import User as SLUser
from surreal.models import Word as SLWord


async def main():
    async with get_session() as session, session.begin():
        await database.connect()
        languages = {}

        for language in await Language.get_all(session=session):
            language = SLLanguage.model_validate(
                await database.db.create("language", {"value": language.value, "display": language.display})
            )
            languages[language.value] = language.id
        for user in await User.get_all(session=session):
            await SLUser.create_or_update(user.id, name=user.name, username=user.username)

        for word in await Word.get_all(session=session):
            await word.awaitable_attrs.translations
            translations = []
            for t in word.translations:
                await t.awaitable_attrs.language
                translation = SLWord.model_validate(
                    await database.db.create("word", {"word": t.translation, "language": languages[t.language.value]})
                )
                for t in translations:
                    await database.db.query(f"RELATE {translation.id} ->translation:ulid() ->{t.id}")
                    await database.db.query(f"RELATE {t.id} ->translation:ulid() ->{translation.id}")
                translations.append(translation)
            await database.db.query(f"RELATE user:{word.user_id} ->know:ulid() ->{translations[0].id}")

        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
