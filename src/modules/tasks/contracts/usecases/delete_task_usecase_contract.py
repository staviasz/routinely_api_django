from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.tasks import DeleteTaskInput, DeleteTaskOutput


class DeleteTaskUsecaseContract(BaseUsecaseContract):
    @abstractmethod
    async def perform(self, data: DeleteTaskInput) -> DeleteTaskOutput:
        pass
