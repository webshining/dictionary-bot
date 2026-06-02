from fastapi import APIRouter, Depends

from api.depends import current_user
from api.models.languages import Response as LanguageResponse
from database import get_session_generator
from database.models import User

router = APIRouter(prefix="/languages", dependencies=[Depends(get_session_generator)])


@router.get("", response_model=list[LanguageResponse])
async def _languages(current_user: User = Depends(current_user)):
    await current_user.awaitable_attrs.languages
    return sorted([l.to_dict() for l in current_user.languages], key=lambda l: l["id"])
