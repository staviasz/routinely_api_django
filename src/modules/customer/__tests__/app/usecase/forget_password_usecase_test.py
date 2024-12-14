from unittest.mock import patch
import pytest
from main.errors.shared.custom_error import CustomError
from main.infra import DispatcherEvents, RepositoryInMemory
from modules.customer import (
    CustomerAggregate,
    ForgotPasswordEvent,
    CacheForgetPasswordCode,
)
from modules.customer.app.usecases.forget_password_usecase import ForgetPasswordUsecase


class ForgetPasswordRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


@pytest.mark.asyncio
class TestForgetPasswordUsecase:
    def setup_method(self):
        self.repository = ForgetPasswordRepositoryInMemory()
        self.cache = CacheForgetPasswordCode()
        self.event = ForgotPasswordEvent()
        self.dispatcher = DispatcherEvents()
        self.usecase = ForgetPasswordUsecase(
            self.repository, self.cache, self.event, self.dispatcher
        )
        self.email = "G0s7B@example.com"
        self.user = CustomerAggregate(
            {
                "id": None,
                "email": self.email,
                "password": "@Teste123",
                "accepted_terms": True,
                "name": "Teste",
            }
        )

    async def test_perform_not_found_email(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"email": "G0s7B@example.com"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["email not found."],
        }

    async def test_perform_set_code_in_cache(self):
        self.repository.list_data.append(self.user)

        await self.usecase.perform({"email": self.email})

        code = self.cache.get(self.email)

        assert code
        assert len(code) == 6
        assert code.isdigit()

    async def test_set_correct_payload_in_event(self):
        self.repository.list_data.append(self.user)

        await self.usecase.perform({"email": self.email})

        payload = self.event.get_payload()

        assert payload["name"] == self.user.name
        assert payload["email"] == self.user.email
        assert payload["code"]

    async def test_perform_success(self):
        self.repository.list_data.append(self.user)

        with patch.object(self.dispatcher, "dispatch") as mock_dispatch:
            account_id = await self.usecase.perform({"email": self.email})

            mock_dispatch.assert_called_once_with(self.event)

        assert account_id
        assert account_id["account_id"] == self.user.id
