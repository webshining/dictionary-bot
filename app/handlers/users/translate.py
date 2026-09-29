import json

from aiogram import Bot, F
from aiogram.types import Message

from loader import _
from surreal.base import current_session
from surreal.models import User, Word

from ..routes import user_router as router
from .languages import _languages


@router.message(F.text, ~F.text.startswith("/"))
async def translate(message: Message, bot: Bot, user: User):
    session = current_session.get()

    text = message.text.lower()
    await user.awaitable_attrs.languages

    if not user.languages:
        await message.answer(_("You haven't added any languages to translate into yet."))
        return await _languages(message, user)

    translations = []
    for language in user.languages:
        translation = (await bot.translator.translate(text, language.value)).lower()
        word = Word.model_validate(await session.create("word", {"word": translation, "language": language.id}))
        for t in translations:
            await session.query(f"RELATE {t.id} ->translation:ulid() ->{word.id}")
            await session.query(f"RELATE {word.id} ->translation:ulid() ->{t.id}")
        translations.append(word)

    if translations:
        await session.query(f"RELATE {user.id} ->know:ulid() ->{translations[0].id}")

    await message.answer(f'<pre language="json">{json.dumps([t.model_dump() for t in translations], indent=4, ensure_ascii=False)}</pre>')
