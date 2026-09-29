from pydantic import BaseModel, Field


class WordResponse(BaseModel):
    id: str
    word: str
    language: str


class ReviewRequest(BaseModel):
    quality: int = Field(ge=0, le=5)
