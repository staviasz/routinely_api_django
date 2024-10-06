import pytest
from main.errors.shared import CustomError
from modules.customer.domain.models import InputCustomerAggregateModel
from .customer_aggregate import CustomerAggregate


class TestCustomerAggregate:
    def test_raise_errors(self):
        with pytest.raises(CustomError) as e:
            CustomerAggregate({"id": "None"})

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in CustomerAggregate is invalid.",
                "The id in CustomerEntity is invalid.",
                "The name is required.",
                "The name must be between 3 and 70 characters and only letters",
                "The terms must be accepted.",
                "The id in AccountEntity is invalid.",
                "The email is required.",
                "The email is invalid.",
                "The password is required.",
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
            ],
        }

    def test_customer_aggregate(self) -> None:
        props: InputCustomerAggregateModel = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Test",
            "accepted_terms": True,
            "email": "test@example.com",
            "password": "@Teste1",
        }

        customer_aggregate = CustomerAggregate(props)
        assert customer_aggregate.to_dict == {
            "id": props["id"],
            "name": props["name"],
            "accepted_terms": props["accepted_terms"],
            "account": {
                "id": props["id"],
                "email": props["email"],
                "password": props["password"],
            },
        }