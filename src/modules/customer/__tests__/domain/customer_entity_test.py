import pytest
from main.errors import CustomError
from modules.customer.domain import CustomerEntity


class TestCustomerEntity:
    def test_raise_exception(self):
        with pytest.raises(CustomError) as e:
            CustomerEntity({"id": "None", "name": "T", "accepted_terms": False})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in CustomerEntity is invalid.",
                "The name must be between 3 and 70 characters and only letters",
                "The terms must be accepted.",
            ],
        }

    def test_accepted_terms_invalid(self):
        with pytest.raises(CustomError) as e:
            CustomerEntity({"name": "Teste", "accepted_terms": "False"})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["The accepted_terms is required."],
        }

    def test_valid_customer_entity(self):
        customer_entity = CustomerEntity({"name": "Teste", "accepted_terms": True})
        assert customer_entity.name == "Teste"
        assert customer_entity.accepted_terms
