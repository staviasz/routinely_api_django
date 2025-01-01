from modules.customer import (
    ForgetPasswordUsecaseContract,
    ForgetPasswordUsecase,
    CacheForgetPasswordCode,
    ForgotPasswordEvent,
    dispatcher_customer,
)
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)


def forget_password_usecase_factory() -> ForgetPasswordUsecaseContract:
    repository = repository_customer_factory()
    cache = CacheForgetPasswordCode()
    event = ForgotPasswordEvent()
    dispatcher = dispatcher_customer
    return ForgetPasswordUsecase(
        repository=repository, cache=cache, event=event, dispatcher=dispatcher
    )
