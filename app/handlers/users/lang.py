from contextlib import suppress

from aiogram import F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.keyboards import LangKeyboard
from loader import _, i18n
from surreal.models import User

from ..routes import user_router as router


@router.message(Command("lang"))
async def _lang(message: Message, user: User):
    languages = [(l, l.capitalize()) for l in i18n.available_locales]
    await message.answer(
        _("Select language:"),
        reply_markup=LangKeyboard.keyboard("settings", languages, [user.lang]),
    )


@router.callback_query(LangKeyboard.filter(F.data == "settings"))
async def _lang_callback(call: CallbackQuery, callback_data: LangKeyboard, user: User):
    await user.change_lang(callback_data.lang)

    languages = [(l, l.capitalize()) for l in i18n.available_locales]
    with suppress(Exception):
        await call.message.edit_text(
            _("Select language:", locale=user.lang), reply_markup=LangKeyboard.keyboard("settings", languages, [user.lang])
        )
