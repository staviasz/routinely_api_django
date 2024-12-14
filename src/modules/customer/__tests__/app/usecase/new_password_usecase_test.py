import pytest
from main.errors.shared.custom_error import CustomError
from main.infra.repository_in_memory import RepositoryInMemory
from modules.customer import CustomerAggregate, NewPasswordUsecase


class NewPasswordRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


@pytest.mark.asyncio
class TestNewPasswordUsecase:
    def setup_method(self):
        self.repository = NewPasswordRepositoryInMemory()
        self.usecase = NewPasswordUsecase(self.repository)
        self.password = "@Last123"
        self.new_password = "@New123"
        self.user = CustomerAggregate(
            {
                "id": None,
                "email": "G0s7B@example.com",
                "password": self.password,
                "accepted_terms": True,
                "name": "Teste",
            }
        )

    async def test_passwords_not_match(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform(
                {
                    "account_id": "1",
                    "password": self.new_password,
                    "confirm_password": "123456",
                }
            )

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Passwords do not match."],
        }

    async def test_raise_Error_if_user_not_found(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform(
                {
                    "account_id": "1",
                    "password": self.new_password,
                    "confirm_password": self.new_password,
                }
            )

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["id not found."],
        }

    async def test_perform(self):
        self.repository.list_data.append(self.user)

        assert self.repository.list_data[0].password == self.password

        await self.usecase.perform(
            {
                "account_id": self.user.id,
                "password": self.new_password,
                "confirm_password": self.new_password,
            }
        )

        user = await self.repository.find_field("id", self.user.id)

        assert user.password == self.new_password
