import asyncio
from datetime import datetime, timedelta
import pytest
from unittest.mock import patch
from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.auth import SessionEntity, JWTAdapter, CreateSessionService


class SessionRepositoryInMemory(RepositoryInMemory[SessionEntity]):
    async def find_session_or_none(self, user_id: str) -> SessionEntity | None:
        sessions = [session for session in self.list_data if session.user_id == user_id]

        return sessions[-1] if sessions else None


@pytest.mark.asyncio
class TestCreateSessionService:
    def setup_method(self):
        self.repository = SessionRepositoryInMemory()
        self.token = JWTAdapter()
        self.service = CreateSessionService(self.repository, self.token)

    async def test_handle_exception_if_user_id_not_found(self):
        with pytest.raises(CustomError) as e:
            await self.service.handle({})

        assert e.value.formate_errors == {
            "code_error": 400,
            "messages_error": ["The user id is required."],
        }

    async def test_handle_success_if_session_not_found(self):
        expires_in = int((datetime.now() + timedelta(minutes=15)).timestamp())

        assert len(self.repository.list_data) == 0

        response = await self.service.handle(
            {"user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b"}
        )

        assert isinstance(response["access_token"], str)
        assert response["expires_in"] == expires_in
        assert isinstance(response["refresh_token"], str)

        assert len(self.repository.list_data) == 1

    async def test_handle_success_if_session_found_not_expired(self):
        expires_in = int((datetime.now() + timedelta(minutes=15)).timestamp())
        user_id = "811c5f65-c4e1-4084-8b15-e8342de5d57b"
        self.repository.list_data.append(SessionEntity({"user_id": user_id}))

        assert len(self.repository.list_data) == 1

        response = await self.service.handle({"user_id": user_id})

        assert isinstance(response["access_token"], str)
        assert response["expires_in"] == expires_in
        assert isinstance(response["refresh_token"], str)

        assert len(self.repository.list_data) == 1

    async def test_handle_success_if_session_found_expired(self):
        user_id = "811c5f65-c4e1-4084-8b15-e8342de5d57b"
        self.repository.list_data.append(
            SessionEntity({"user_id": user_id, "max_expires_at": {"milliseconds": 50}}),
        )

        assert len(self.repository.list_data) == 1
        await asyncio.sleep(0.1)
        expires_in = int((datetime.now() + timedelta(minutes=15)).timestamp())
        response = await self.service.handle({"user_id": user_id})

        assert isinstance(response["access_token"], str)
        assert response["expires_in"] == expires_in
        assert isinstance(response["refresh_token"], str)

        assert len(self.repository.list_data) == 2
