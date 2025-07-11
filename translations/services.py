from django.conf import settings
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


async def detect_language(word: str) -> str:
    client = tr.TranslationServiceAsyncClient(credentials=credentials)
    response = await client.detect_language(content=word, parent=parent, mime_type="text/plain")
    return response.languages[0].language_code
