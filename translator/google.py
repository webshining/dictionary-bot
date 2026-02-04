from google.cloud.translate import TranslationServiceAsyncClient
from google.oauth2.service_account import Credentials


class GoogleTranslator:
    client: TranslationServiceAsyncClient

    def __init__(self, credentials_file: str):
        creds = Credentials.from_service_account_file(credentials_file)
        self.client = TranslationServiceAsyncClient(credentials=creds)

    async def translate(self, text: str, lang: str) -> str:
        res = await self.client.translate_text(
            request={
                "parent": "projects/brain-464016/locations/global",
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": lang,
            }
        )
        return res.translations[0].translated_text
