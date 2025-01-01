from modules.auth import SessionService, RefreshSessionService, JWTAdapter
from modules.auth.factories.infra.repository_session_factory import (
    repository_session_factory,
)


def refresh_session_service_factory() -> SessionService:
    repository = repository_session_factory()
    token = JWTAdapter()
    return RefreshSessionService(repository=repository, token=token)
