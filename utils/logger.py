import json
import logging
import sys

from django.conf import settings
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    level="DEBUG",
    filter=lambda record: record["level"].name in ["DEBUG", "INFO"],
)
logger.add(sys.stderr, level="WARNING")


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "level": record["level"].name,
        "message": record["message"],
    }
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


logger = logger.patch(patching)
logger.add(
    settings.BASE_DIR.joinpath("logs", "app.json"),
    format="{extra[serialized]}",
    rotation="1 day",
    retention="1 month",
)


def setup_logger(name: str) -> None:
    class CustomFilter(logging.Filter):
        def filter(self, record):
            return "Failed to fetch updates" not in record.getMessage()

    log = logging.getLogger(name)
    log.addFilter(CustomFilter())
    log.setLevel(logging.ERROR)


setup_logger("aiogram")
setup_logger("aiogram.dispatcher")
