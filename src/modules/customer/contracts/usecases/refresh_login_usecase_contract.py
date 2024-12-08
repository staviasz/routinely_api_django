from abc import abstractmethod

from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types import RefreshLoginInput, RefreshLoginOutput


class RefreshLoginUsecaseContract(
    BaseUsecaseContract[RefreshLoginInput, RefreshLoginOutput]
):
    @abstractmethod
    async def perform(self, data: RefreshLoginInput) -> RefreshLoginOutput:
        pass
