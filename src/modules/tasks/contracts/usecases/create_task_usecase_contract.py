from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.tasks import CreateTaskInput, CreateTaskOutput


class CreateTaskUsecaseContract(BaseUsecaseContract[CreateTaskInput, CreateTaskOutput]):

    @abstractmethod
    async def perform(self, data: CreateTaskInput) -> CreateTaskOutput:
        pass
