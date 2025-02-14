from abc import ABC, abstractmethod

from main.contracts import BaseUsecaseContract
from modules.customer import RegisterCustomerInput, RegisterCustomerOutput


class RegisterUsecaseContract(
    BaseUsecaseContract[RegisterCustomerInput, RegisterCustomerOutput]
):
    @abstractmethod
    async def perform(self, data: RegisterCustomerInput) -> RegisterCustomerOutput:
        pass
