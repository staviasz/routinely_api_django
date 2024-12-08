from modules.auth.services.base_session_tokens import SessionService
from modules.auth.types import SessionInput, SessionOutput


class CreateSessionService(SessionService):

    async def handle(self, payload: SessionInput) -> SessionOutput:

        response = await self.create_session(payload)
        return response
