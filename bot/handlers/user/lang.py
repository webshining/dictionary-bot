from contextlib import suppress

from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from django.utils.translation import override

from bot.keyboards import LangKeyboard, get_menu_keyboard
from users.models import User
from ..routes import user_router as router
from ...loader import bot
from ...text import Text


@router.message(Command("lang"))
@router.message(F.text == Text.LANGUAGE_BUTTON.value)
async def lang_handler(message: Message, user: User):
    await message.delete()
    await message.answer(str(Text.SELECT_LANGUAGE).format(user.language_code),
                         reply_markup=LangKeyboard.keyboard(user.language_code))


@router.callback_query(LangKeyboard.filter())
async def lang_callback_handler(call: CallbackQuery, callback_data: LangKeyboard, user: User, state: FSMContext):
    await call.answer()
    user.language_code = callback_data.lang
    await user.asave(update_fields=["language_code"])
    with override(user.language_code):
        with suppress(Exception):
            await call.message.edit_text(str(Text.SELECT_LANGUAGE).format(user.language_code),
                                         reply_markup=LangKeyboard.keyboard(user.language_code))
        with suppress(Exception):
            language_message = await state.get_value("language_message")
            await bot.delete_message(chat_id=call.message.chat.id, message_id=language_message)
        with suppress(Exception):
            message = await call.message.answer(str(Text.LANGUAGE_CHANGED), reply_markup=get_menu_keyboard())
            await state.update_data(language_message=message.message_id)
