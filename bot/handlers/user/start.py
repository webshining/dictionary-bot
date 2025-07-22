from aiogram.filters import Command
from aiogram.types import Message

from ..routes import user_router as router
from ...keyboards import get_menu_keyboard
from ...text import Text


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.delete()
    await message.answer(Text.START.value.format(message.from_user.full_name), reply_markup=get_menu_keyboard())
