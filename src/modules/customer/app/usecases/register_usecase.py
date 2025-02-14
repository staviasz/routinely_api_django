from main.contracts import EventBaseClass, DispatcherContract
from main.errors import CustomError, ConflictError
from modules.customer.contracts import (
    RegisterUsecaseContract,
    RegisterRepositoryContract,
)
from modules.customer import (
    RegisterCustomerOutput,
    RegisterCustomerInput,
    CustomerAggregate,
)


class RegisterUsecase(RegisterUsecaseContract):
    def __init__(
        self,
        repository: RegisterRepositoryContract,
        event: EventBaseClass,
        dispatcher: DispatcherContract,
    ) -> None:
        self.repository = repository
        self.event = event
        self.dispatcher = dispatcher

    async def perform(self, data: RegisterCustomerInput) -> RegisterCustomerOutput:
        aggregate_customer = CustomerAggregate(data)

        email = aggregate_customer.email
        has_email_in_use = await self.repository.find_field_or_none("email", email)
        if has_email_in_use:
            raise CustomError(ConflictError("email"))

        await self.repository.create(aggregate_customer)

        self.event.set_payload(
            {
                "name": aggregate_customer.name,
                "email": email,
                "callback_url": data["callback_url"],
            }
        )
        self.dispatcher.dispatch(self.event)

        return
