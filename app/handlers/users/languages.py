from contextlib import suppress

from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards import LangKeyboard
from loader import _
from surreal.models import Language, User

from ..routes import user_router as router


@router.message(Command("languages"))
async def _languages(message: Message, user: User):
    languages = await Language.get_all()
    await user.awaitable_attrs.languages

    await message.answer(
        _("Select languages for translate:"),
        reply_markup=LangKeyboard.keyboard("translate", [(l.id.id, l.display) for l in languages], [l.id.id for l in user.languages]),
    )


@router.callback_query(LangKeyboard.filter(F.data == "translate"))
async def _languages_callback(call: CallbackQuery, callback_data: LangKeyboard, user: User):
    await user.awaitable_attrs.languages
    await user.toggle_language(callback_data.lang)
    await user.awaitable_attrs.languages

    languages = await Language.get_all()
    with suppress(Exception):
        await call.message.edit_text(
            _("Select languages for translate:"),
            reply_markup=LangKeyboard.keyboard("translate", [(l.id.id, l.display) for l in languages], [l.id.id for l in user.languages]),
        )
