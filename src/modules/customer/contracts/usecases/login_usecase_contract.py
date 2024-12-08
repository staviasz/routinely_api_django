from abc import abstractmethod

from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types import LoginInput, LoginOutput


class LoginUsecaseContract(BaseUsecaseContract[LoginInput, LoginOutput]):
    @abstractmethod
    async def perform(self, data: LoginInput) -> LoginOutput:
        pass
