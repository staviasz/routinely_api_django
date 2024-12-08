from unittest.mock import Mock, patch
import pytest
from main.errors.shared.custom_error import CustomError
from main.infra.repository_in_memory import RepositoryInMemory
from modules.auth import SessionServiceContract
from modules.customer import LoginUsecase, CustomerAggregate, HashAdapter


class LoginRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


authMock = Mock(spec=SessionServiceContract)


@pytest.mark.asyncio
class TestLoginUseCase:
    def setup_method(self):
        self.repository = LoginRepositoryInMemory()
        self.auth = authMock
        self.hash = HashAdapter()
        self.usecase = LoginUsecase(self.repository, self.auth, self.hash)
        self.password = "@Teste123"
        self.password_hash = self.hash.hash(self.password)
        self.user = CustomerAggregate(
            {
                "id": None,
                "email": "G0s7B@example.com",
                "password": self.password,
                "accepted_terms": True,
                "name": "Teste",
            }
        )
        self.user.password = self.password_hash

    async def test_raise_error_if_email_not_found(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"email": "G0s7B@example.com", "password": ""})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["email not found."],
        }

    async def test_call_hash(self):
        data = {"email": "G0s7B@example.com", "password": self.password}

        self.repository.list_data.append(self.user)

        with patch.object(self.hash, "verify") as mock_hash:
            await self.usecase.perform(data)
            mock_hash.assert_called_once_with(self.password, self.password_hash)

    async def test_raise_error_if_password_not_match(self):
        data = {"email": "G0s7B@example.com", "password": "password"}

        self.repository.list_data.append(self.user)

        with pytest.raises(CustomError) as e:
            await self.usecase.perform(data)

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 401,
            "messages_error": ["Invalid credentials"],
        }

    async def test_call_auth_with_correct_payload(self):
        data = {"email": "G0s7B@example.com", "password": self.password}

        self.repository.list_data.append(self.user)

        with patch.object(self.auth, "handle") as mock_auth:
            await self.usecase.perform(data)
            mock_auth.assert_called_once_with(
                {"id": self.user.id, "email": self.user.email}
            )

    async def test_login_successfully(self):
        data = {"email": "G0s7B@example.com", "password": self.password}
        auth = {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_in": 3600,
        }

        self.repository.list_data.append(self.user)
        self.auth.handle.return_value = {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_in": 3600,
        }

        response = await self.usecase.perform(data)

        assert response == auth
