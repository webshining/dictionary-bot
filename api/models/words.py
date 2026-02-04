from pydantic import BaseModel, model_validator


class Request(BaseModel):
    init_data: str


class TranslationResponse(BaseModel):
    id: int
    translation: str
    language: str

    @model_validator(mode="before")
    def extract_language_name(cls, values):
        values["language"] = values["language"]["name"]
        return values


class Response(BaseModel):
    id: int
    translations: list[TranslationResponse]
