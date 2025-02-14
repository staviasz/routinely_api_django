import re
from pydantic import BaseModel, EmailStr, Field


class ConfirmEmailSchema(BaseModel):
    email: EmailStr = Field(...)
    callback_url: str = Field(...)
