from modules.tasks import (
    CreateTaskUsecaseContract,
    CreateTaskInput,
    CreateTaskOutput,
    TaskEntity,
    CreateTaskRepositoryContract,
)


class CreateTaskUsecase(CreateTaskUsecaseContract):
    def __init__(self, repository: CreateTaskRepositoryContract) -> None:
        self.repository = repository

    async def perform(self, data: CreateTaskInput) -> CreateTaskOutput:
        entity = TaskEntity({**data})
        await self.repository.create(entity)
        return {"id": entity.id}
