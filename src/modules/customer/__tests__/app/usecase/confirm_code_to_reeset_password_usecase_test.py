from unittest.mock import Mock, patch
import pytest
from main.errors.shared.custom_error import CustomError
from main.infra.repository_in_memory import RepositoryInMemory
from modules.auth import SessionServiceContract
from modules.customer import LoginUsecase, CustomerAggregate
from modules.customer.app.usecases.confirm_code_to_reset_password_usecase import (
    ConfirmCodeToResetPasswordUsecase,
)
from modules.customer.infra.cache.forget_password_code import CacheForgetPasswordCode


class ConfirmCodeRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


@pytest.mark.asyncio
class TestLoginUseCase:
    def setup_method(self):
        self.repository = ConfirmCodeRepositoryInMemory()
        self.cache = CacheForgetPasswordCode()
        self.usecase = ConfirmCodeToResetPasswordUsecase(self.repository, self.cache)
        self.email = "G0s7B@example.com"
        self.code = "123456"
        self.user = CustomerAggregate(
            {
                "id": None,
                "email": self.email,
                "password": "@Teste123",
                "accepted_terms": True,
                "name": "Teste",
            }
        )

    async def test_raise_error_if_email_not_found(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"email": "G0s7B@example.com", "code": "123456"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["email not found."],
        }

    async def test_raise_error_if_code_not_found(self):
        self.repository.list_data.append(self.user)

        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"email": self.email, "code": self.code})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Expired code."],
        }

    async def test_raise_error_if_code_not_match(self):
        self.repository.list_data.append(self.user)
        self.cache.set(self.email, self.code)

        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"email": self.email, "code": "654321"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Invalid code."],
        }

    async def test_perform_success(self):
        self.repository.list_data.append(self.user)
        self.cache.set(self.email, self.code)

        await self.usecase.perform({"email": self.email, "code": self.code})

        assert self.user.is_active
        assert self.repository.list_data[0] == self.user
