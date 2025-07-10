import asyncio

from django.core.management.base import (
    BaseCommand,
)

from bot.start import start


class Command(BaseCommand):
    help = "Start bot"

    def handle(self, *args, **options):
        asyncio.run(start())
