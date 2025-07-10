from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import alogin
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from ninja import Router
from ninja.security import django_auth
from pydantic import BaseModel

from translations.services import translate, detect_language
from users.models import User

router = Router()


class InitRequest(BaseModel):
    tgWebAppData: str


class DictionaryRequest(BaseModel):
    name: str
    source_lang: str
    target_lang: str


class WordRequest(BaseModel):
    word: str


# Get cookies
@router.post("/init")
async def init_handler(request: HttpRequest, body: InitRequest):
    if check_webapp_signature(settings.TELEGRAM_BOT_TOKEN, body.tgWebAppData):
        user_telegram_id = safe_parse_webapp_init_data(settings.TELEGRAM_BOT_TOKEN, body.tgWebAppData).user.id
        user = await User.objects.aget(telegram_id=user_telegram_id)
        await alogin(request, user)
        return JsonResponse({"message": "Success"})
    return JsonResponse({"message": "Unauthorized"}, status=401)


# GET dictionaries
@router.get("/dictionaries", auth=django_auth)
async def dictionaries_handler(request: HttpRequest):
    dictionaries = await sync_to_async(list)(request.user.dictionaries.prefetch_related("words").all())
    for i, dictionary in enumerate(dictionaries):
        dictionaries[i] = model_to_dict(dictionary)
        dictionaries[i]['words'] = [model_to_dict(w) for w in dictionary.words.all()]
    return JsonResponse({"dictionaries": dictionaries})


# GET dictionary by id
@router.get("/dictionaries/{id}", auth=django_auth)
async def dictionary_handler(request: HttpRequest, id: int):
    dictionary = await request.user.dictionaries.prefetch_related("words").aget(id=id)
    dict_data = model_to_dict(dictionary)
    dict_data["words"] = [model_to_dict(i) for i in dictionary.words.all()]
    return JsonResponse({"dictionary": dict_data})


# CREATE word in dictionary
@router.post("/dictionaries/{id}/words", auth=django_auth)
async def word_create_handler(request: HttpRequest, id: int, body: WordRequest):
    dictionary = await request.user.dictionaries.prefetch_related("words").aget(id=id)

    lang = await detect_language(body.word)
    source_word = body.word.strip()
    if lang is not dictionary.source_lang:
        source_word = await translate(source_word, dictionary.source_lang)
    target_word = body.word.strip()
    if lang is not dictionary.target_lang:
        target_word = await translate(target_word, dictionary.target_lang)

    await dictionary.words.acreate(word=source_word, translate=target_word)


# DELETE word from dictionary
@router.delete("/dictionaries/{dictionary_id}/words/{word_id}", auth=django_auth)
async def word_delete_handler(request: HttpRequest, dictionary_id: int, word_id: int):
    pass


# CREATE dictionary
@router.post("/dictionaries", auth=django_auth)
async def dictionary_create_handler(request: HttpRequest, body: DictionaryRequest):
    await request.user.dictionaries.acreate(name=body.name, source_lang=body.source_lang, target_lang=body.target_lang)
    return JsonResponse({"message": "Success"})


# DELETE dictionary by id
@router.delete("/dictionaries/{id}", auth=django_auth)
async def dictionary_delete_handler(request: HttpRequest, id: int):
    dictionary = await request.user.dictionaries.aget(id=id)
    await dictionary.adelete()
    return JsonResponse({"message": "Success"})


# UPDATE dictionary by id
@router.put("/dictionaries/{id}", auth=django_auth)
async def dictionary_update_handler(request: HttpRequest, id: int, body: DictionaryRequest):
    dictionary = await request.user.dictionaries.aget(id=id)
    dictionary.name = body.name
    dictionary.source_lang = body.source_lang
    dictionary.target_lang = body.target_lang
    await dictionary.asave()
    return JsonResponse({"message": "Success"})
