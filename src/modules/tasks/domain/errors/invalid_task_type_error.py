from typing import get_args
from main.errors.shared.custom_error import CustomErrorAbstract
from modules.tasks.domain.models.task_type import TaskType


class InvalidTaskTypeError(CustomErrorAbstract):
    def __init__(self) -> None:
        list_types = list(get_args(TaskType))
        super().__init__(
            code_error=400,
            message_error=f"The Type must be one of: {", ".join(list_types)}",
        )
