from abc import abstractmethod
from datetime import datetime
from typing import Any, cast
from main.errors import CustomError, BadRequestError
from modules.auth.domain.entity import SessionEntity
from modules.auth.types import SessionInput, SessionOutput
from modules.auth.contracts import (
    CreateSessionRepositoryContract,
    SessionServiceContract,
    JWTContract,
)


class SessionService(SessionServiceContract):
    def __init__(
        self, repository: CreateSessionRepositoryContract, token: JWTContract
    ) -> None:
        self.repository = repository
        self.token = token

    @abstractmethod
    async def handle(self, payload: SessionInput) -> SessionOutput:
        pass

    async def create_session(self, payload: SessionInput) -> SessionOutput:

        user_id = payload.get("user_id")
        if not user_id:
            raise CustomError(BadRequestError("The user id is required."))

        entity_session = SessionEntity({"user_id": user_id})
        entity_session_dict = entity_session.to_dict()

        payload_token = self.__payload_token(payload, entity_session_dict["id"])  # type: ignore
        token = self.token.encode(payload_token)

        payload_refresh_token = {
            "session_id": entity_session.id,
            "iat": entity_session_dict["created_at"],
            "exp": entity_session_dict["expires_at"],
        }
        refresh_token = self.token.encode(payload_refresh_token)

        session = await self.repository.find_session_or_none(user_id)
        if not session or session.expires_at < datetime.now():  # type: ignore
            print("update")
            await self.repository.create(entity_session)

        return {
            "access_token": token,
            "refresh_token": refresh_token,
            "expires_in": payload_token["exp"],
        }

    def __payload_token(self, data: SessionInput, session_id: str) -> dict[str, Any]:
        current_time = int(datetime.now().timestamp())
        expires_in = 15 * 60
        return {
            **data,
            "session_id": session_id,
            "iat": current_time,
            "exp": current_time + expires_in,
        }
