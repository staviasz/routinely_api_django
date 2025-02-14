from modules.customer import ConfirmEmailUsecaseContract, ConfirmEmailUsecase
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)


def confirm_email_usecase_factory() -> ConfirmEmailUsecaseContract:
    repository = repository_customer_factory()
    return ConfirmEmailUsecase(repository=repository)
