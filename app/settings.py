from pathlib import Path

import dj_database_url
from environs import env

env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)#sz6y4#0jq#xjjxxo3&57&hp#vwf#fwb5vs)l&*%2n&!$4yk^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = [
    "localhost",
    "http://localhost:3000",
    "calm-composed-gobbler.ngrok-free.app",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://calm-composed-gobbler.ngrok-free.app",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://calm-composed-gobbler.ngrok-free.app",
]
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "bot",
    "ai",
    "dictionary",
    "api",
    "translations",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middlewares.UserLanguageMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    # {
    #     "BACKEND": "django.template.backends.jinja2.Jinja2",
    #     "DIRS": [BASE_DIR.joinpath("webapp", "templates")],
    #     "OPTIONS": {
    #         "environment": "app.jinja2.environment",
    #     },
    # },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
DATABASE_URL = env.str("DATABASE_URL", default="sqlite:///database.db")
DATABASES = {"default": dj_database_url.config(default=DATABASE_URL)}

# Auth
AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
USE_I18N = True
LANGUAGES = [
    ("en", "English"),
    ("ru", "Русский"),
    ("uk", "Українська"),
]
LOCALE_PATHS = [BASE_DIR.joinpath("locale")]

# Timezone
TIME_ZONE = "UTC"
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.joinpath("staticfiles")
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Telegram
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
GOOGLE_AI_API_KEY = env.str("GOOGLE_AI_API_KEY")
