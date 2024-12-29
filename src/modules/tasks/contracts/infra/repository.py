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


class ListTasksRepositoryContract(FindFieldContract[T]):
    pass


class TaskRepositoryContract(
    CreateTaskRepositoryContract,
    UpdateTaskRepositoryContract,
    DeleteTaskRepositoryContract,
):
    pass
