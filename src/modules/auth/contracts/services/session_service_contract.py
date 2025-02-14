from abc import abstractmethod
from main.contracts.services.base_services import BaseServiceContract
from modules.auth.types import SessionInput, SessionOutput


class SessionServiceContract(BaseServiceContract[SessionInput, SessionOutput]):

    @abstractmethod
    async def handle(self, data: SessionInput) -> SessionOutput:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> SessionInput:
        pass
