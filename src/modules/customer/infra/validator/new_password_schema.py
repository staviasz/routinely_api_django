import re
from pydantic import BaseModel, Field, field_validator, model_validator


class NewPasswordValidator(BaseModel):
    account_id: str = Field(...)
    password: str = Field(..., min_length=6, max_length=70)
    confirm_password: str = Field(..., min_length=6, max_length=70)

    @field_validator("password", "confirm_password")
    def validate_password(cls, v):
        regex = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*=])[a-zA-Z\d!@#$%&*=]{6,}$"
        )
        if not re.match(regex, v):
            raise ValueError(
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            )
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("The confirm password must match the password.")
        return self
