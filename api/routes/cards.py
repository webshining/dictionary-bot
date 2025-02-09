from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.schemas import DictionaryResponse
from data.config import DIR, TELEGRAM_BOT_TOKEN
from database import AsyncSession, get_session_depends
from database.models import Dictionary

router = APIRouter()
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get("/{dictionary_id}/init", response_class=HTMLResponse)
async def _cards_init():
    html_content = """
        <html>
            <head>
                <script>
                    var url = window.location.href;
                    const fragment = window.location.hash;
                    const searchParams = new URLSearchParams(fragment.substring(1));
                    url = url.replace('/init', '').replace(fragment, "");
                    const newUrl = new URL(url);            
                    for (const [key, value] of searchParams) {
                        newUrl.searchParams.append(key, value);
                    }
                    window.location.replace(`${newUrl}${fragment}`);
                </script>
            </head>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@router.get("/{dictionary_id}", response_class=HTMLResponse)
async def _card_page(request: Request, dictionary_id: int, session: AsyncSession = Depends(get_session_depends)):
    tgWebAppData = request.query_params.get("tgWebAppData")
    if not check_webapp_signature(TELEGRAM_BOT_TOKEN, tgWebAppData):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = safe_parse_webapp_init_data(TELEGRAM_BOT_TOKEN, tgWebAppData).user.id
    dictionary = await Dictionary.get_by(id=dictionary_id, user_id=user_id, session=session)
    if not dictionary:
        raise HTTPException(status_code=404, detail="Not found")

    await session.refresh(dictionary, ["words"])
    return templates.TemplateResponse(
        name="cards.html",
        request=request,
        context={"dictionary": DictionaryResponse.model_validate(dictionary).model_dump()},
    )
