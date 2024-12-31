from typing import Generic, Protocol
from main.contracts.infra.repository_infra_contract import (
    CreateContract,
    FindFieldContract,
    UpdateContract,
    DeleteContract,
)
from modules.tasks.domain.task_entity import TaskEntity


T = TaskEntity


class CreateTaskRepositoryContract(CreateContract[T]):
    pass


class UpdateTaskRepositoryContract(FindFieldContract[T], UpdateContract[T]):
    pass


class DeleteTaskRepositoryContract(DeleteContract[T]):
    pass


class ListTasksRepositoryContract(Protocol):
    async def find_tasks_by_user_id_and_month_and_year(
        self, user_id: str, month: int, year: int
    ) -> list[T]:
        pass


class TaskRepositoryContract(
    CreateTaskRepositoryContract,
    UpdateTaskRepositoryContract,
    DeleteTaskRepositoryContract,
):
    pass
