from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types import (
    NewPasswordInput,
    NewPasswordOutput,
)


class NewPasswordUsecaseContract(
    BaseUsecaseContract[NewPasswordInput, NewPasswordOutput]
):
    @abstractmethod
    async def perform(self, data: NewPasswordInput) -> NewPasswordOutput:
        pass
