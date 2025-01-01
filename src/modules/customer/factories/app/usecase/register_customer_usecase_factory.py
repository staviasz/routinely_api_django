from modules.customer import (
    RegisterUsecaseContract,
    RegisterUsecase,
    CreatedCustomerEvent,
    dispatcher_customer,
)
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)


def register_customer_usecase_factory() -> RegisterUsecaseContract:
    repository = repository_customer_factory()
    event = CreatedCustomerEvent()
    dispatcher = dispatcher_customer
    return RegisterUsecase(repository=repository, event=event, dispatcher=dispatcher)
