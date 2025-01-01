from modules.customer import LoginUsecaseContract, LoginUsecase
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)
from modules.auth import create_session_service_factory


def login_usecase_factory() -> LoginUsecaseContract:
    repository = repository_customer_factory()
    auth = create_session_service_factory()
    return LoginUsecase(repository=repository, auth=auth)
