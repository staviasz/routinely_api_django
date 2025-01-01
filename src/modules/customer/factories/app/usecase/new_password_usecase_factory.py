from modules.customer import NewPasswordUsecaseContract, NewPasswordUsecase
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)


def new_password_usecase_factory() -> NewPasswordUsecaseContract:
    repository = repository_customer_factory()
    return NewPasswordUsecase(repository=repository)
