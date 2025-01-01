from modules.auth import (
    CreateSessionRepositoryContract,
    JWTContract,
    SessionInput,
    SessionOutput,
)
from modules.auth.services.base_session_tokens import SessionService


class CreateSessionService(SessionService):
    def __init__(
        self, repository: CreateSessionRepositoryContract, token: JWTContract
    ) -> None:
        super().__init__(repository, token)

    async def handle(self, payload: SessionInput) -> SessionOutput:

        response = await self.create_session(payload)
        return response
