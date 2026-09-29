from pathlib import Path

from environs import Env

env = Env()
env.read_env()

DIR = Path(__file__).absolute().parent.parent
DEV = env.bool("DEV", default=True)

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")

WEBHOOK_URL = env.str("WEBHOOK_URL", default=None)
WEBHOOK_PATH = env.str("WEBHOOK_PATH", default=None)
WEBHOOK_SERVER_HOST = env.str("WEBHOOK_SERVER_HOST", default=None)
WEBHOOK_SERVER_PORT = env.int("WEBHOOK_SERVER_PORT", default=None)
WEBHOOK_SERVER_SECRET = env.str("WEBHOOK_SERVER_SECRET", default=None)

SERVER_HOST = env.str("SERVER_HOST", default="localhost")
SERVER_PORT = env.int("SERVER_PORT", default=4000)

RD_URI = env.str("RD_URI", default=None)

DB_URI = env.str("DB_URI", default="sqlite+aiosqlite:///database.sqlite3")

SURREAL_URL = env.str("SURREAL_URL")
SURREAL_USERNAME = env.str("SURREAL_USERNAME")
SURREAL_PASSWORD = env.str("SURREAL_PASSWORD")
SURREAL_NAMESPACE = env.str("SURREAL_NAMESPACE")
SURREAL_DATABASE = env.str("SURREAL_DATABASE")

I18N_PATH = f"{DIR}/data/locales"
I18N_DOMAIN = "bot"
