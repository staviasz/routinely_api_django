import pytest

from main.errors.shared import CustomError
from modules.customer.domain.aggregate.value_objects import EmailValueObject


class TestEmailValueObject:
    def test_all_errors(self):
        with pytest.raises(CustomError) as e:
            EmailValueObject("")

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The email is required.",
                "The email is invalid.",
            ],
        }

    def test_email_invalid(self):
        with pytest.raises(CustomError) as e:
            EmailValueObject("teste")

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": ["The email is invalid."],
        }

    def test_email_valid(self):
        email = EmailValueObject("5hjQp@example.com")
        assert email.value == "5hjQp@example.com"
