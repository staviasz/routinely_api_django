from pydantic import BaseModel, EmailStr, Field, field_validator


class ConfirmCodeToResetPasswordSchema(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)
    account_id: str = Field(...)

    @field_validator("code")
    def validate_code(cls, v):
        if not v.isdigit():
            raise ValueError("Code must be a number")
        return v
