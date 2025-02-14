from unittest.mock import Mock

import pytest
from main.infra import BaseValidationPydantic
from modules.customer.app import RegisterCustomerController
from modules.customer.contracts import RegisterUsecaseContract
from modules.customer.infra import RegisterCustomerSchema

usecase = Mock(spec=RegisterUsecaseContract)
validator = BaseValidationPydantic(RegisterCustomerSchema)
controller = RegisterCustomerController(usecase=usecase, validator=validator)


@pytest.mark.asyncio
class TestRegisterCustomerController:
    async def test_no_body_in_request(self):
        response = await controller.execute({})

        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "name: Field required",
                "email: Field required",
                "password: Field required",
                "confirmed_password: Field required",
                "accepted_terms: Field required",
                "callback_url: Input should be a valid string",
            ]
        }

    async def test_invalid_data(self):
        response = await controller.execute(
            {
                "body": {
                    "name": "in",
                    "email": "invalid",
                    "password": "invalidd",
                    "confirmed_password": "invalidd",
                    "accepted_terms": False,
                },
            }
        )

        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "name: String should have at least 3 characters",
                "email: value is not a valid email address: An email address must have an @-sign.",
                "password: Must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 8 characters long",
                "confirmed_password: Must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 8 characters long",
                "accepted_terms: Terms must be accepted",
                "callback_url: Input should be a valid string",
            ]
        }

    async def test_different_passwords(self):
        response = await controller.execute(
            {
                "query": {"callback_url": "any_url"},
                "body": {
                    "name": "valid",
                    "email": "test@test.com",
                    "password": "@Teste123",
                    "confirmed_password": "@Teste1234",
                    "accepted_terms": True,
                },
            }
        )

        assert response["status"] == 400
        assert response["body"] == {"message": ["Passwords: are not equal"]}

    async def test_call_usecase(self):
        data = {
            "query": {"callback_url": "any_url"},
            "body": {
                "name": "valid",
                "email": "test@test.com",
                "password": "@Teste123",
                "confirmed_password": "@Teste123",
                "accepted_terms": True,
            },
        }

        await controller.execute({"body": data["body"], "query": data["query"]})

        usecase.perform.assert_called_once_with({**data["body"], **data["query"]})

    async def test_success(self):
        data = {
            "query": {"callback_url": "any_url"},
            "body": {
                "name": "valid",
                "email": "test@test.com",
                "password": "@Teste123",
                "confirmed_password": "@Teste123",
                "accepted_terms": True,
            },
        }
        response = await controller.execute(
            {"body": data["body"], "query": data["query"]}
        )

        usecase.perform.assert_called_with({**data["body"], **data["query"]})
        assert response["status"] == 201
        assert response["body"] == {}
