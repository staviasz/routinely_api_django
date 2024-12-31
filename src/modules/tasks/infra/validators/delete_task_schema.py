from pydantic import BaseModel, Field


class DeleteTaskSchema(BaseModel):
    id: str = Field(...)
