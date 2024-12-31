from typing import Optional, TypedDict
from modules.tasks.domain import TaskCategories, TaskType, Weekday


class ListTasksInput(TypedDict):
    user_id: str
    month: Optional[int]
    year: Optional[int]


class TaskModel(TypedDict):
    id: str
    type: TaskType
    name: str
    date_time: str
    description: str
    category: TaskCategories
    weekdays: Optional[list[Weekday]]
    finally_datetime: Optional[str]


class ListTasksOutput(TypedDict):
    tasks: list[TaskModel]
