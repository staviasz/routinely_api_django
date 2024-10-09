from main.errors import CustomError, ConflitError
from modules.customer.contracts import (
    RegisterUsecaseContract,
    RegisterRepositoryContract,
)
from modules.customer.domain import InputCustomerAggregateModel, CustomerAggregate


class RegisterUsecase(RegisterUsecaseContract):
    def __init__(self, repository: RegisterRepositoryContract) -> None:
        self.repository = repository

    def perform(self, data: InputCustomerAggregateModel) -> None:
        aggregate_customer = CustomerAggregate(data)

        email = aggregate_customer.email
        has_email_in_use = self.repository.find_field_or_none("email", email)
        if has_email_in_use:
            raise CustomError(ConflitError("email"))

        self.repository.create(aggregate_customer)
        return
