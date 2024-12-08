from datetime import datetime, timedelta
import pytest
from unittest.mock import patch
from main.errors.shared.custom_error import CustomError
from main.infra.repository_in_memory import RepositoryInMemory
from modules.auth import SessionEntity, JWTAdapter, CreateSessionService


class SessionRepositoryInMemory(RepositoryInMemory[SessionEntity]):
    pass


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

    async def test_handle_success(self):
        expires_in = int((datetime.now() + timedelta(minutes=15)).timestamp())
        response = await self.service.handle(
            {"user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b"}
        )

        assert isinstance(response["access_token"], str)
        assert response["expires_in"] == expires_in
        assert isinstance(response["refresh_token"], str)
