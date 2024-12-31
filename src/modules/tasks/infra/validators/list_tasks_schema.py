from typing import Optional
from pydantic import BaseModel, Field, StrictInt, field_validator


class ListTasksSchema(BaseModel):
    user_id: str = Field(..., min_length=1)
    month: Optional[StrictInt] = Field(
        None, le=12, ge=1, description="Month must be between 1 and 12"
    )
    year: Optional[StrictInt] = Field(
        None, ge=2000, description="Year must be greater than 2000"
    )
