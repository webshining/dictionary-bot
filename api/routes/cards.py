from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from data.config import DIR

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get('')
async def cards(request: Request):
    return templates.TemplateResponse(request=request, name="cards.html")
