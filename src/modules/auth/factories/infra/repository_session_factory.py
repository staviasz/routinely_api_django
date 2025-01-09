from modules.auth import SessionRepositoryContract, RepositorySession


def repository_session_factory() -> SessionRepositoryContract:
    return RepositorySession()
