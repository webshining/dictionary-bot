import csv
import io

from aiogram import html
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from asgiref.sync import sync_to_async
from django.utils.translation import gettext as _

from users.models import User

from ..routes import admin_router as router


@router.message(Command("users"))
async def _users(message: Message):
    users = await sync_to_async(list)(User.objects.all())
    text, file = await _get_users_data(users)
    text = _("<b>Users:</b>") + text
    await message.answer(text)
    await message.answer_document(BufferedInputFile(file, "users.csv"))


async def _get_users_data(users: list[User]):
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(["id", "telegram_id", "first_name", "last_name", "username", "telegram_username"])

    for user in users:
        writer.writerow(
            [user.id, user.telegram_id, user.first_name, user.last_name, user.username, user.telegram_username]
        )

    file.seek(0)
    file_bytes = io.BytesIO(file.getvalue().encode())
    file_bytes.seek(0)
    return _get_users_text(users), file_bytes.getvalue()


def _get_users_text(users: list[User]) -> str:
    if not users:
        return "\n" + _("No users🫡")

    text = ""
    for user in users:
        name = html.quote(f"{user.first_name} {user.last_name}")
        text += f"\n|name: <b>{name}</b>"
    return text
