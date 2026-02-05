from pydantic import BaseModel


class Request(BaseModel):
    init_data: str
