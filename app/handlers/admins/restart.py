import os

from aiogram import types
from aiogram.filters import Command

from ..routes import admin_router as router


@router.message(Command("restart"))
async def _restart_command(message: types.Message) -> None:
    await message.answer("Restarting and updating the bot...")
    os.system("git pull --rebase")
    os.system("supervisorctl restart dictionary")
