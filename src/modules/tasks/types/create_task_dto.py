from typing import Optional, TypedDict
from modules.tasks.domain import TaskCategories, TaskType, Weekday


class CreateTaskInput(TypedDict, total=False):
    user_id: str
    type: TaskType
    name: str
    date_time: str
    description: str
    category: TaskCategories
    weekdays: Optional[list[Weekday]]
    finally_datetime: Optional[str]


class CreateTaskOutput(TypedDict):
    id: str
