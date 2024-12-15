from pydantic import BaseModel, Field


class RefreshLoginSchema(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
