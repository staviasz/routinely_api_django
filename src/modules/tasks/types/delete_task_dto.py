from typing import Optional, TypeAlias, TypedDict
from modules.tasks.domain import TaskCategories, TaskType, Weekday


class DeleteTaskInput(TypedDict):
    id: str


DeleteTaskOutput: TypeAlias = None
