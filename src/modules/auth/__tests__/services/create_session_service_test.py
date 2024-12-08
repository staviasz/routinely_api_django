from datetime import datetime
import pytest
from unittest.mock import patch
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

    async def test_handle_find_field_or_none_return_none(self):
        payload = {"id": "any_id"}
        with patch.object(self.repository, "find_field_or_none") as mock_repo_find:
            with patch.object(self.repository, "delete") as mock_repo_delete:
                mock_repo_find.return_value = None
                await self.service.handle(payload)

        mock_repo_find.assert_called_once_with("id", "any_id")
        mock_repo_delete.assert_not_called()

    async def test_handle_find_field_or_none_return_item(self):
        payload = {"id": "811c5f65-c4e1-4084-8b15-e8342de5d57b"}
        self.repository.list_data.append(
            SessionEntity({"id": payload["id"], "token": "any_token"})
        )
        await self.service.handle(payload)

        assert len(self.repository.list_data) == 1

    async def test_handle_success(self):
        expires_in = int(datetime.now().timestamp()) + 15 * 60
        response = await self.service.handle({"id": None})

        entity = self.repository.list_data[0]
        assert isinstance(response["access_token"], str)
        assert response["expires_in"] == expires_in
        assert response["refresh_token"] == entity.to_dict()["token"]
