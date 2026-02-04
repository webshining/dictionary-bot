from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import LangKeyboard
from database.models import Language, User
from loader import _

from ..routes import user_router as router


@router.message(Command("languages"))
async def _languages(message: Message, user: User, session: AsyncSession):
    await user.awaitable_attrs.languages
    languages = await Language.get_all(session=session)
    await message.answer(
        _("Select languages for translate:"),
        reply_markup=LangKeyboard.keyboard("translate", [(l.id, l.name.capitalize()) for l in languages], [l.id for l in user.languages]),
    )


@router.callback_query(LangKeyboard.filter(F.data == "translate"))
async def _languages_callback(call: CallbackQuery, callback_data: LangKeyboard, user: User, session: AsyncSession):
    await user.awaitable_attrs.languages

    language = await Language.get(callback_data.lang, session=session)
    if language in user.languages:
        user.languages.remove(language)
    else:
        user.languages.append(language)
    await session.commit()

    languages = await Language.get_all(session=session)
    try:
        await call.message.edit_text(
            _("Select languages for translate:"),
            reply_markup=LangKeyboard.keyboard(
                "translate", [(l.id, l.name.capitalize()) for l in languages], [l.id for l in user.languages]
            ),
        )
    except Exception:
        pass
