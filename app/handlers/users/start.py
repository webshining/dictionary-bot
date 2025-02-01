from aiogram import html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import MenuKeyboard
from loader import _

from ..routes import user_router as router


@router.message(CommandStart())
async def _start(message: Message, state: FSMContext):
    await state.set_state(None)

    text = _("Hello {}").format(html.quote(message.from_user.full_name))
    await message.answer(text, reply_markup=MenuKeyboard.keyboard())
