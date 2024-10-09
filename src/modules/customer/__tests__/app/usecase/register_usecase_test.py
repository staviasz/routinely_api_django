from unittest.mock import patch
import pytest
from main.errors import CustomError
from main.infra import RepositoryInMemory
from modules.customer.app import RegisterUsecase
from modules.customer.domain import CustomerAggregate


class CustomerRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


class TestRegisterUsecase:
    def setup_method(self):
        self.repository = CustomerRepositoryInMemory()
        self.usecase = RegisterUsecase(self.repository)

    def test_invalid_data(self):

        with pytest.raises(CustomError) as e:
            self.usecase.perform({})

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The name is required.",
                "The name must be between 3 and 70 characters and only letters",
                "The terms must be accepted.",
                "The email is required.",
                "The email is invalid.",
                "The password is required.",
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            ],
        }

    def test_email_exists(self):
        data = {
            "name": "Teste",
            "email": "G0s7B@example.com",
            "password": "@Teste123",
            "accepted_terms": True,
        }

        self.repository.list_data.append(CustomerAggregate(data))

        with patch.object(self.repository, "find_field_or_none") as mock_perform:
            with pytest.raises(CustomError) as e:
                self.usecase.perform(data)

            custom_error = e.value
            assert custom_error.formated_errors == {
                "code_error": 409,
                "messages_error": ["Conflit: The email already exists."],
            }

            mock_perform.assert_called_once_with("email", "G0s7B@example.com")
