from modules.auth import SessionRepositoryContract, RepositorySession


def repository_session_factory() -> SessionRepositoryContract:
    db_client = None
    return RepositorySession(db_client)
