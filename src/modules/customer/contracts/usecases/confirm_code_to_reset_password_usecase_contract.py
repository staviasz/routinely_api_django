from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types import ConfirmCodeToResetPasswordInput


class ConfirmCodeToResetPasswordUsecaseContract(
    BaseUsecaseContract[ConfirmCodeToResetPasswordInput, None]
):
    @abstractmethod
    async def perform(self, data: ConfirmCodeToResetPasswordInput) -> None:
        pass
