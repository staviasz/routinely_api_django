from datetime import datetime
from typing import cast
from modules.tasks import (
    ListTasksUsecaseContract,
    ListTasksInput,
    ListTasksOutput,
    ListTasksRepositoryContract,
)
from modules.tasks.types.list_tasks_dto import TaskModel


class ListTaskUsecase(ListTasksUsecaseContract):
    def __init__(self, repository: ListTasksRepositoryContract) -> None:
        self.repository = repository

    async def perform(self, data: ListTasksInput) -> ListTasksOutput:
        now = datetime.now()
        month = data.get("month") or now.month
        year = data.get("year") or now.year

        tasks = await self.repository.find_tasks_by_user_id_and_month_and_year(
            data["user_id"], month, year
        )
        result: list[TaskModel] = []

        if len(tasks):
            for item in tasks:
                item_dict = item.to_dict()
                del item_dict["user_id"]
                result.append(cast(TaskModel, item_dict))

        return {"tasks": result}
