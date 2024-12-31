from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from modules.tasks import TaskCategories, TaskType, Weekday


class CreateTaskSchema(BaseModel):
    user_id: str = Field(...)
    description: str = Field(..., max_length=1000, min_length=10)
    category: TaskCategories = Field(...)
    name: str = Field(..., min_length=10, max_length=50)
    type: TaskType = Field(...)
    date_time: str = Field(...)
    weekdays: Optional[list[Weekday]] = Field(None)
    finally_datetime: Optional[str] = Field(None)

    @field_validator("date_time", "finally_datetime")
    def validate_date_time(cls, v):
        if v:
            date_formats = [
                "%Y/%m/%d",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%dT%H:%M:%S",
            ]

            for date_format in date_formats:
                try:
                    datetime.strptime(v, date_format)
                    return v
                except (ValueError, TypeError):
                    continue

            raise ValueError(
                "Invalid date format, expected formats YYYY/MM/DD, YYYY/MM/DD HH:MM, YYYY/MM/DD HH:MM:SS, YYYY/MM/DDTHH:MM:SS"
            )
