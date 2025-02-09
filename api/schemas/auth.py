from pydantic import BaseModel


class AuthRequest(BaseModel):
    initData: str
