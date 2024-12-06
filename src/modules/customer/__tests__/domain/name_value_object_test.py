import pytest
from main.errors import CustomError
from modules.customer.domain import NameValueObject


class TestNameValueObject:
    def test_all_errors(self):
        with pytest.raises(CustomError) as error:
            NameValueObject("")

        custom_error = error.value
        print(custom_error.formate_errors)
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The name is required.",
                "The name must be between 3 and 70 characters and only letters",
            ],
        }

    def test_name_length_invalid(self):
        with pytest.raises(CustomError) as error:
            NameValueObject("T")

        custom_error = error.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The name must be between 3 and 70 characters and only letters"
            ],
        }

    def test_name_invalid(self):
        with pytest.raises(CustomError) as error:
            NameValueObject("Teste1")

        custom_error = error.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The name must be between 3 and 70 characters and only letters"
            ],
        }

    def test_name_valid(self):
        name = NameValueObject("Teste")
        assert name.value == "Teste"
