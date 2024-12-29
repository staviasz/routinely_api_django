from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.tasks import UpdateTaskInput, UpdateTaskOutput


class UpdateTaskUsecaseContract(BaseUsecaseContract):
    @abstractmethod
    async def perform(self, data: UpdateTaskInput) -> UpdateTaskOutput:
        pass
