import re
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class RegisterCustomerSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=70)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=70)
    confirmed_password: str = Field(..., min_length=8, max_length=70)
    accepted_terms: bool = Field(...)
    callback_url: str = Field(...)

    @field_validator("password", "confirmed_password")
    def validate_passwords(cls, v):
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(regex, v):
            raise ValueError(
                "Must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 8 characters long"
            )
        return v

    @field_validator("accepted_terms")
    def validate_terms(cls, v):
        if not v:
            raise ValueError("Terms must be accepted")
        return v

    @model_validator(mode="after")
    def check_passwords_equal(cls, values):
        dict_values = values.__dict__
        if dict_values["password"] != dict_values["confirmed_password"]:
            raise ValueError("Passwords: are not equal")
        return values
