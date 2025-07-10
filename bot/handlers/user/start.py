from aiogram.filters import Command
from aiogram.types import Message
from django.utils.translation import gettext as _

from ..routes import user_router as router


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(_("Hello <b>{}</b>").format(message.from_user.full_name))
