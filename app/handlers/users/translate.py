import json

from aiogram import Bot, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Translation, User, Word
from loader import _

from ..routes import user_router as router
from .languages import _languages


@router.message(~F.text.startswith("/"))
async def translate(message: Message, bot: Bot, user: User, session: AsyncSession):
    text = message.text.lower()
    await user.awaitable_attrs.languages
    await user.awaitable_attrs.words

    if not user.languages:
        await message.answer(_("You haven't added any languages to translate into yet."))
        return await _languages(message, user, session)

    word = Word()
    translations = []
    for language in user.languages:
        translation = (await bot.translator.translate(text, language.name)).lower()
        translations.append({"translation": translation, "language": language.name})
        word.translations.append(Translation(translation=translation, language=language))

    if translations:
        user.words.append(word)
        await session.commit()

    await message.answer(f'<pre language="json">{json.dumps(translations, indent=4, ensure_ascii=False)}</pre>')
