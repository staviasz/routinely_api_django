from modules.customer import (
    ConfirmCodeToResetPasswordUsecaseContract,
    ConfirmCodeToResetPasswordUsecase,
    Cache,
)
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)


def confirm_code_to_reset_password_usecase_factory() -> (
    ConfirmCodeToResetPasswordUsecaseContract
):
    repository = repository_customer_factory()
    cache = Cache()
    return ConfirmCodeToResetPasswordUsecase(repository=repository, cache=cache)
