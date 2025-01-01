from modules.auth import refresh_session_service_factory
from modules.customer import RefreshLoginUsecaseContract, RefreshLoginUsecase


def refresh_login_usecase_factory() -> RefreshLoginUsecaseContract:
    auth = refresh_session_service_factory()
    return RefreshLoginUsecase(auth=auth)
