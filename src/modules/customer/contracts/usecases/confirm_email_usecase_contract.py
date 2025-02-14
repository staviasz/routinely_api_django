from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types import ConfirmEmailInput, ConfirmEmailOutput


class ConfirmEmailUsecaseContract(
    BaseUsecaseContract[ConfirmEmailInput, ConfirmEmailOutput]
):
    @abstractmethod
    async def perform(self, data: ConfirmEmailInput) -> ConfirmEmailOutput:
        pass
