from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.schemas import WordResponse
from data.config import DIR
from database import AsyncSession, get_session_depends
from database.models import Dictionary

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get("/{id}", response_class=HTMLResponse)
async def _card_page(request: Request, id: int, session: AsyncSession = Depends(get_session_depends)):
    dictionary = await Dictionary.get(id=id, session=session)
    await session.refresh(dictionary, ["words"])
    words = [WordResponse.model_validate(w).model_dump() for w in dictionary.words]

    return templates.TemplateResponse(name="cards.html", request=request, context={"words": words})
