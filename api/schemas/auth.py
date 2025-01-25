from pydantic import BaseModel


class AuthSchema(BaseModel):
    data: str
