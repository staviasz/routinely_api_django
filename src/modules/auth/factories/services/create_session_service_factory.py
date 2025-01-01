from modules.auth import SessionService, CreateSessionService, JWTAdapter
from modules.auth.factories.infra.repository_session_factory import (
    repository_session_factory,
)


def create_session_service_factory() -> SessionService:
    repository = repository_session_factory()
    token = JWTAdapter()
    return CreateSessionService(repository=repository, token=token)
