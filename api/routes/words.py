from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.schemas import WordRequest, WordResponse
from api.services import get_current_user
from data.config import DIR
from database import AsyncSession, get_session_depends
from database.models import Dictionary, Word

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get("/{dictionary_id}")
async def _words(
    request: Request,
    dictionary_id: int,
    session: AsyncSession = Depends(get_session_depends),
    accept: str = Header(),
):
    if "application/json" in accept:
        user_id = await get_current_user(request.headers.get("initData"))
        dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
        words = await dictionary.get_words()
        return [WordResponse.model_validate(word).model_dump() for word in words]
    dictionary = await Dictionary.get(id=dictionary_id, session=session)
    await session.refresh(dictionary, ["words"])
    return templates.TemplateResponse(name="words.html", request=request)


@router.put("/{dictionary_id}/{word_id}")
async def _word_update_know(
    dictionary_id: int,
    word_id: int,
    body: WordRequest,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_depends),
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    word = await Word.get_by(dictionary_id=dictionary_id, id=word_id, session=session)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    if body.know:
        word.known_count += 1
    else:
        word.unknown_count += 1
    await session.commit()

    return True


@router.delete("/{dictionary_id}/{word_id}")
async def _word_delete(
    dictionary_id: int,
    word_id: int,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_depends),
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    await Word.delete_by(id=word_id, dictionary_id=dictionary_id, session=session)
    return True
