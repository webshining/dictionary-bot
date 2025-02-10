from fastapi import APIRouter, Depends, HTTPException

from api.schemas import WordProcessRequest, WordRequest, WordResponse
from api.services import get_current_user
from database import AsyncSession, get_session_depends
from database.models import Dictionary, Word
from utils import translate_word

router = APIRouter()


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


@router.put("/{dictionary_id}/{word_id}")
async def _word_process(
    dictionary_id: int,
    word_id: int,
    body: WordProcessRequest,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_depends),
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")
    word = await Word.get_by(id=word_id, dictionary_id=dictionary_id, session=session)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    if body.know:
        await Word.update(id=word_id, known_count=word.known_count + 1, session=session)
    else:
        await Word.update(id=word_id, unknown_count=word.unknown_count + 1, session=session)
    return True


@router.post("/{dictionary_id}", response_model=WordResponse)
async def _word_create(
    dictionary_id: int,
    body: WordRequest,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_depends),
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")

    translate = (await translate_word(body.word))[0][0]
    word = await Word.create(dictionary_id=dictionary_id, **body.model_dump(), translate=translate, session=session)
    return WordResponse.model_validate(word).model_dump()
