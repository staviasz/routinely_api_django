import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class ConfirmEmailSchema(BaseModel):
    email: EmailStr = Field(...)
    callback_url: str = Field(...)

    @field_validator("callback_url")
    def validate_callback_url(cls, v):
        regex = re.compile(
            r"""^https?:\/\/
                (?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|localhost)
                (:\d{1,5})?
                (?:\/[a-zA-Z0-9\-._~:/?#[\]@!$&'()*+,;=%]*)?$""",
            re.VERBOSE,
        )
        if not regex.match(v):
            raise ValueError("Invalid URL")
        return v
