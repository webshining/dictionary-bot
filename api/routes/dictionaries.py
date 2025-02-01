from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.templating import Jinja2Templates

from api.schemas import DictionaryRequest, DictionaryResponse
from api.services import get_current_user
from data.config import DIR
from database import AsyncSession, get_session_depends
from database.models import Dictionary

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get("/{dictionary_id}", response_model=DictionaryResponse)
async def _dictionary(
    dictionary_id: int, user_id: int = Depends(get_current_user), session: AsyncSession = Depends(get_session_depends)
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    await session.refresh(dictionary, ["words"])
    return DictionaryResponse.model_validate(dictionary).model_dump()


@router.put("/{dictionary_id}", response_model=DictionaryResponse)
async def _dictionary_update(
    dictionary_id: int,
    body: DictionaryRequest,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_depends),
):
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    await session.refresh(dictionary, ["words"])
    dictionary.name = body.name
    await session.commit()

    return DictionaryResponse.model_validate(dictionary).model_dump()
