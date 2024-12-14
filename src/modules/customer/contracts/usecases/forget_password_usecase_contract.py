from abc import abstractmethod
from main.contracts.usecases.base_usecase_contract import BaseUsecaseContract
from modules.customer.types.forget_password_dto import (
    ForgetPasswordInput,
    ForgetPasswordOutput,
)


class ForgetPasswordUsecaseContract(
    BaseUsecaseContract[ForgetPasswordInput, ForgetPasswordOutput]
):
    @abstractmethod
    async def perform(self, data: ForgetPasswordInput) -> ForgetPasswordOutput:
        pass
