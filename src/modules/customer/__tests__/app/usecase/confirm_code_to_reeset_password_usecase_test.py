from unittest.mock import Mock
import pytest
from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.customer import CustomerAggregate
from modules.customer.app.usecases.confirm_code_to_reset_password_usecase import (
    ConfirmCodeToResetPasswordUsecase,
)
from modules.customer.infra.cache.cache import Cache


class ConfirmCodeRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


@pytest.mark.asyncio
class TestConfirmCodeUseCase:
    def setup_method(self):
        self.repository = ConfirmCodeRepositoryInMemory()
        self.cache = Mock(spec=Cache)
        self.usecase = ConfirmCodeToResetPasswordUsecase(self.repository, self.cache)
        self.email = "G0s7B@example.com"
        self.code = "123456"
        self.user = CustomerAggregate(
            {
                "email": self.email,
                "password": "@Teste123",
                "accepted_terms": True,
                "name": "Teste",
            }
        )

    async def test_raise_error_if_email_not_found(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"id": self.user.id, "code": "123456"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["id not found."],
        }

    async def test_raise_error_if_code_not_found(self):
        self.cache.get.return_value = None
        self.repository.list_data.append(self.user)

        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"id": self.user.id, "code": self.code})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Expired code."],
        }

    async def test_raise_error_if_code_not_match(self):
        self.repository.list_data.append(self.user)
        self.cache.get.return_value = self.code

        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"id": self.user.id, "code": "654321"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Invalid code."],
        }

    async def test_perform_success(self):
        self.repository.list_data.append(self.user)
        self.cache.get.return_value = self.code

        await self.usecase.perform({"id": self.user.id, "code": self.code})

        assert self.user.is_active
        assert self.repository.list_data[0] == self.user
