from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.schemas import DictionaryResponse, WordRequest
from data.config import DIR
from database import AsyncSession, get_session_depends
from database.models import Dictionary, Word

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.post("/{id}")
async def _word(id: int, body: WordRequest, session: AsyncSession = Depends(get_session_depends)):
    word = await Word.get(id=id, session=session)
    if body.know:
        word.known_count += 1
    else:
        word.unknown_count += 1
    await session.commit()

    return True


@router.delete("/{dictionary_id}/{word_id}")
async def _word_delete(dictionary_id, word_id: int, session: AsyncSession = Depends(get_session_depends)):
    await Word.delete_by(id=word_id, dictionary_id=dictionary_id, session=session)
    return True


@router.put("/{dictionary_id}/{word_id}")
async def _word_delete(dictionary_id, word_id: int, session: AsyncSession = Depends(get_session_depends)):
    await Word.delete_by(id=word_id, dictionary_id=dictionary_id, session=session)
    return True


@router.get("/{id}", response_class=HTMLResponse)
async def _words_page(request: Request, id: int, session: AsyncSession = Depends(get_session_depends)):
    dictionary = await Dictionary.get(id=id, session=session)
    await session.refresh(dictionary, ["words"])

    return templates.TemplateResponse(
        name="words.html",
        request=request,
        context={"dictionary": DictionaryResponse.model_validate(dictionary).model_dump()},
    )
