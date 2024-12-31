from modules.tasks import (
    DeleteTaskUsecaseContract,
    DeleteTaskRepositoryContract,
    DeleteTaskInput,
    DeleteTaskOutput,
)


class DeleteTaskUsecase(DeleteTaskUsecaseContract):
    def __init__(self, repository: DeleteTaskRepositoryContract) -> None:
        self.repository = repository

    async def perform(self, data: DeleteTaskInput) -> DeleteTaskOutput:
        await self.repository.delete("id", data["id"])
