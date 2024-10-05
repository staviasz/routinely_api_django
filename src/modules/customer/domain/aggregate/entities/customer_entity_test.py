import pytest
from main.errors.shared import CustomError
from .customer_entity import CustomerEntity


class TestCustomerEntity:
    def test_raise_exception(self):
        with pytest.raises(CustomError) as e:
            CustomerEntity({"id": "None", "name": "T", "accepted_terms": False})

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in CustomerEntity is invalid.",
                "The name must be between 3 and 70 characters and only letters",
                "The terms must be accepted.",
            ],
        }
