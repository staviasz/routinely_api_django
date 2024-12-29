from typing import Optional, TypedDict
from modules.tasks.domain import TaskCategories, TaskType, Weekday


class TaskModel(TypedDict, total=False):
    id: Optional[str]
    user_id: str
    type: TaskType
    name: str
    date_time: str
    category: TaskCategories
    description: str
    weekdays: Optional[list[Weekday]]
    finally_datetime: Optional[str]
