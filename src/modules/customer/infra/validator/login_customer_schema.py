import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginValidator(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=70)
    remember_me: Optional[bool] = Field(default=False)

    @field_validator("password")
    def validate_password(cls, v):
        regex = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*=])[a-zA-Z\d!@#$%&*=]{6,}$"
        )
        if not re.match(regex, v):
            raise ValueError(
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            )
        return v
