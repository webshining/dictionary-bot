from django.conf import settings
from django.core.cache import cache
from google.cloud import translate as tr
from google.oauth2.service_account import Credentials

credentials = Credentials.from_service_account_file(settings.BASE_DIR.joinpath("translator.json"))
parent = f"projects/brain-464016/locations/global"


async def translate(word: str | list[str], target_lang: str) -> list[str]:
    client = tr.TranslationServiceAsyncClient(credentials=credentials)
    response = await client.translate_text(
        request={
            "parent": parent,
            "contents": word if type(word) is list else [word],
            "mime_type": "text/plain",
            "target_language_code": target_lang,
        }
    )
    return [t.translated_text for t in response.translations]


async def get_supported_languages():
    cache_key = "supported_languages"
    data = await cache.aget(cache_key)
    if data is not None:
        return data

    client = tr.TranslationServiceAsyncClient(credentials=credentials)
    response = await client.get_supported_languages(parent=parent, display_language_code="en")

    languages = [
        {"code": lang.language_code, "name": lang.display_name}
        for lang in response.languages
    ]

    await cache.aset(cache_key, languages, 60 * 60 * 24)
    return languages


async def detect_language(word: str) -> str:
    client = tr.TranslationServiceAsyncClient(credentials=credentials)
    response = await client.detect_language(content=word, parent=parent, mime_type="text/plain")
    return response.languages[0].language_code
