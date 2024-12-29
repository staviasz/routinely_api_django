from typing import Optional, TypeAlias, TypedDict
from modules.tasks.domain import TaskCategories, TaskType, Weekday


class UpdateTaskInput(TypedDict, total=False):
    id: str
    user_id: str
    type: Optional[TaskType]
    name: Optional[str]
    date_time: Optional[str]
    description: Optional[str]
    category: Optional[TaskCategories]
    weekdays: Optional[list[Weekday]]
    finally_datetime: Optional[str]


UpdateTaskOutput: TypeAlias = None
