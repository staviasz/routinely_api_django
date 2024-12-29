from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.tasks import ListTasksInput, ListTasksOutput


class ListTasksUsecaseContract(BaseUsecaseContract[ListTasksInput, ListTasksOutput]):

    @abstractmethod
    async def perform(self, data: ListTasksInput) -> ListTasksOutput:
        pass
