import pytest

from main.errors import CustomError
from modules.customer.domain import PasswordValueObject


class TestPasswordValueObject:
    def test_raise_error(self):
        with pytest.raises(CustomError) as error:
            PasswordValueObject("")

        custom_error = error.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The password is required.",
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            ],
        }

    def test_password_invalid(self):
        with pytest.raises(CustomError) as error:
            PasswordValueObject("Teste1")

        custom_error = error.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            ],
        }

    def test_password_valid(self):
        vo = PasswordValueObject("@Teste123")
        assert vo.value == "@Teste123"
