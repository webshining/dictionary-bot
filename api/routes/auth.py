from fastapi import APIRouter

from api.schemas import AuthSchema
from api.services import is_telegram

router = APIRouter()


@router.post("")
async def is_auth(body: AuthSchema):
    print(is_telegram(body.data))
    return is_telegram(body.data)
