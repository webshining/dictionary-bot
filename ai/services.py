import google.genai as genai
from django.conf import settings

from ai.types import LemmatizeResponse, TranslateResponse

client = genai.Client(api_key=settings.GOOGLE_AI_API_KEY)


async def lemmatize(words: str | list[str]) -> list[str]:
    prompt = f"Correct the words and lemmatize without changing the language."
    response = await client.aio.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, "\n\n", ",".join(words)],
        config={
            "response_mime_type": "application/json",
            "response_schema": LemmatizeResponse,
        },
    )
    return response.parsed.words


async def word_data(word: str) -> TranslateResponse:
    prompt = "Find up to 3 synonyms and make up to 3 sentences with a word and wrapp this word in <u></u>."
    response = await client.aio.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, word],
        config={
            "response_mime_type": "application/json",
            "response_schema": TranslateResponse,
        },
    )
    return response.parsed
