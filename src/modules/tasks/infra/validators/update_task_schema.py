from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from modules.tasks import TaskCategories, TaskType, Weekday


class UpdateTaskSchema(BaseModel):
    id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    type: Optional[TaskType] = Field(None)
    name: Optional[str] = Field(None, min_length=10, max_length=50)
    date_time: Optional[str] = Field(None)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category: Optional[TaskCategories] = Field(None)
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

    @model_validator(mode="after")
    def validate_if_exist_fields_to_update(cls, values):
        dict_values = values.__dict__
        if not any(
            [
                dict_values.get("type"),
                dict_values.get("name"),
                dict_values.get("date_time"),
                dict_values.get("description"),
                dict_values.get("category"),
                dict_values.get("weekdays"),
                dict_values.get("finally_datetime"),
            ]
        ):
            raise ValueError("No fields to update")

        return values
