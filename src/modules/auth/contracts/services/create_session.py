from abc import abstractmethod
from typing import Any, Dict, TypeVar
from main.contracts.services.base_services import BaseServiceContract
from modules.auth.types import SessionInput, SessionOutput


class CreateSessionServiceContract(BaseServiceContract[SessionInput, SessionOutput]):

    @abstractmethod
    async def handle(self, data: SessionInput) -> SessionOutput:
        pass
