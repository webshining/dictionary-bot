from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from data.config import DIR
from database import AsyncSession, get_session_depends

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get("/{id}", response_class=HTMLResponse)
async def _card_page(request: Request, id: int, session: AsyncSession = Depends(get_session_depends)):
    return templates.TemplateResponse(name="cards.html", request=request)
