from pydantic import BaseModel, EmailStr, Field


class ForgetPasswordSchema(BaseModel):
    email: EmailStr = Field(..., min_length=3, max_length=255)
