from abc import ABC, abstractmethod

from main.contracts import BaseUsecaseContract
from modules.customer.domain import InputCustomerAggregateModel


class RegisterUsecaseContract(BaseUsecaseContract[InputCustomerAggregateModel]):
    @abstractmethod
    def perform(self, data: InputCustomerAggregateModel) -> None:
        pass
