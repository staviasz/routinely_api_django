from main.contracts import EventBaseClass, DispatcherContract
from main.errors import CustomError, ConflictError
from modules.customer.contracts import (
    RegisterUsecaseContract,
    RegisterRepositoryContract,
    HashContract,
)
from modules.customer.domain import InputCustomerAggregateModel, CustomerAggregate


class RegisterUsecase(RegisterUsecaseContract):
    def __init__(
        self,
        repository: RegisterRepositoryContract,
        hash: HashContract,
        event: EventBaseClass,
        dispatcher: DispatcherContract,
    ) -> None:
        self.repository = repository
        self.event = event
        self.dispatcher = dispatcher
        self.hash = hash

    async def perform(self, data: InputCustomerAggregateModel) -> None:
        aggregate_customer = CustomerAggregate(data)

        email = aggregate_customer.email
        has_email_in_use = await self.repository.find_field_or_none("email", email)
        if has_email_in_use:
            raise CustomError(ConflictError("email"))

        password_hash = self.hash.hash(aggregate_customer.password)
        aggregate_customer.password = password_hash

        await self.repository.create(aggregate_customer)

        self.event.set_payload({"name": aggregate_customer.name, "email": email})
        self.dispatcher.dispatch(self.event)

        return
