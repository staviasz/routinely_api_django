from datetime import datetime
from typing import Optional, cast
from modules.tasks import (
    UpdateTaskUsecaseContract,
    UpdateTaskRepositoryContract,
    UpdateTaskInput,
    UpdateTaskOutput,
    TaskEntity,
    TaskModel,
)


class UpdateTaskUsecase(UpdateTaskUsecaseContract):
    def __init__(self, repository: UpdateTaskRepositoryContract) -> None:
        self.repository = repository

    async def perform(self, data: UpdateTaskInput) -> UpdateTaskOutput:
        repo_entity = await self.repository.find_field("id", data["id"])

        new_data = {
            **repo_entity.to_dict(),
            **data,
            "user_id": repo_entity.user_id,
            "date_time": self.__date_to_domain(
                repo_entity.date_time, data.get("date_time")
            ),
            "finally_datetime": self.__date_to_domain(
                repo_entity.finally_datetime, data.get("finally_datetime")
            ),
        }

        entity = TaskEntity(cast(TaskModel, new_data))

        return await self.repository.update(entity)

    def __date_to_domain(
        self, repo_date: Optional[datetime], input_date: Optional[str]
    ) -> None | str:

        if input_date:
            return input_date

        return repo_date.strftime("%Y/%m/%d %H:%M:%S") if repo_date else None
