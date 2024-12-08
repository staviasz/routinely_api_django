from datetime import datetime
from typing import Any
from modules.auth.domain.entity import SessionEntity
from modules.auth.types import SessionInput, SessionOutput
from modules.auth.contracts import (
    CreateSessionRepositoryContract,
    CreateSessionServiceContract,
    JWTContract,
)


class CreateSessionService(CreateSessionServiceContract):
    def __init__(
        self, repository: CreateSessionRepositoryContract, token: JWTContract
    ) -> None:
        self.repository = repository
        self.token = token

    async def handle(self, payload: SessionInput) -> SessionOutput:

        exists_token = await self.repository.find_field_or_none("id", payload["id"])
        if exists_token:
            await self.repository.delete("id", payload["id"])

        payload_token = self.__payload_token(payload)
        token = self.token.encode(payload_token)
        refresh_token = self.token.encode(self.__payload_refresh_token(payload))

        await self.repository.create(
            SessionEntity({"token": refresh_token, "id": None})
        )

        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "expires_in": payload_token["exp"],
        }

    def __payload_token(self, data: SessionInput) -> dict[str, Any]:
        current_time = int(datetime.now().timestamp())
        expires_in = 15 * 60
        return {
            **data,
            "iat": current_time,
            "exp": current_time + expires_in,
        }

    def __payload_refresh_token(self, data: SessionInput) -> dict[str, Any]:
        current_time = int(datetime.now().timestamp())
        expires_in = 7 * 24 * 60 * 60
        return {
            **data,
            "iat": current_time,
            "exp": current_time + expires_in,
        }
