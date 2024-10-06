import pytest

from main.errors.shared.custom_error import CustomError
from modules.customer.domain.aggregate.entities import AccountEntity


class TestAccoutEntity:
    def test_all_errors(self):
        with pytest.raises(CustomError) as e:
            AccountEntity({"id": "None"})

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in AccountEntity is invalid.",
                "The email is required.",
                "The email is invalid.",
                "The password is required.",
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            ],
        }

    def test_account_entity(self):
        props = {
            "email": "test@test.com",
            "password": "@Teste1",
        }
        account_entity = AccountEntity(props)

        assert account_entity.id is not None
        assert account_entity.email == props["email"]
        assert account_entity.password == props["password"]
