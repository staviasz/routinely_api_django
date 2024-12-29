from typing import get_args
from main.errors.shared.custom_error import CustomErrorAbstract
from modules.tasks.domain.models.task_categories import TaskCategories


class InvalidTaskCategoryError(CustomErrorAbstract):
    def __init__(self) -> None:
        list_types = list(get_args(TaskCategories))
        super().__init__(
            code_error=400,
            message_error=f"The category must be one of: {", ".join(list_types)}",
        )
