from modules.auth import SessionRepositoryContract, SessionEntity


class RepositorySession(SessionRepositoryContract):
    def __init__(self, db_client) -> None:
        self.db_client = db_client

    async def create(self, entity: SessionEntity) -> None:
        return
