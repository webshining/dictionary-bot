import aiohttp
from fake_useragent import UserAgent

ua = UserAgent()


async def translate_word(word: str, target: str = "ru"):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "format": "text",
                "from": "eng",
                "to": target,
                "input": word,
                "options": {
                    "sentenceSplitter": True,
                    "origin": "translation.web",
                    "contextResults": True,
                    "languageDetection": True,
                },
            },
            headers={"User-Agent": ua.random},
        ) as response:
            data = await response.json()
            data = data["contextResults"]["results"][:3]
            translations = [d["translation"] for d in data]
        async with session.get(
            f"https://definition-api.reverso.net/v1/api/definitions/en/{word}?targetLang={target}&maxExpressions=60&showNeighbors=2&expressionDefs=6&wordExpressions=true&synonyms=false",
            headers={"User-Agent": ua.random},
        ) as response:
            data = await response.json()
            data = data["DefsByWord"][0]
            samples = list(get_samples(data["DefsByPos"]))
            expressions = [(e["expression"], e["def"]) for e in data["expressionDefs"][:5]]
        return translations, samples, expressions


def get_samples(defs_by_pos: list):
    for defs in defs_by_pos:
        if defs["Defs"]:
            if defs["Defs"][0]["examples"]:
                yield defs["Defs"][0]["examples"][0]["example"], defs["Pos"]
