import pytest
from main.errors import CustomError
from modules.customer.domain import InputCustomerAggregateModel, CustomerAggregate


class TestCustomerAggregate:
    def setup_method(self):
        self.data = {
            "name": "Test",
            "accepted_terms": True,
            "email": "test@example.com",
            "password": "@Teste1",
        }

        self.customer_aggregate = CustomerAggregate(self.data)

    def test_raise_errors(self):
        with pytest.raises(CustomError) as e:
            CustomerAggregate({"id": "None"})

        custom_error = e.value
        print(custom_error.formate_errors)
        assert custom_error.formate_errors == {
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
        {
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
            ],
        }

    def test_customer_aggregate(self) -> None:
        customer_aggregate = self.customer_aggregate
        assert customer_aggregate.email == self.data["email"]
        assert customer_aggregate.password == self.data["password"]
        assert customer_aggregate.name == self.data["name"]
        assert customer_aggregate.accepted_terms == self.data["accepted_terms"]
        assert customer_aggregate.id is not None
        assert customer_aggregate.is_active is False

    def test_activate(self) -> None:
        customer_aggregate = self.customer_aggregate
        customer_aggregate.activate()
        assert customer_aggregate.is_active is True

    def test_deactivate(self) -> None:
        customer_aggregate = self.customer_aggregate
        customer_aggregate.deactivate()
        assert customer_aggregate.is_active is False

    def test_change_password(self) -> None:
        customer_aggregate = self.customer_aggregate

        with pytest.raises(CustomError) as e:
            customer_aggregate.change_password("@Teste")

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long"
            ],
        }

        customer_aggregate.change_password("@Teste123")
        assert customer_aggregate.password == "@Teste123"
