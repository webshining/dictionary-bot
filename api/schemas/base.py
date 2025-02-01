from pydantic import BaseModel, ConfigDict


class BaseModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
