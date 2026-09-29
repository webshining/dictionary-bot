from pydantic import BaseModel


class LanguageResponse(BaseModel):
    id: str
    value: str
    display: str
