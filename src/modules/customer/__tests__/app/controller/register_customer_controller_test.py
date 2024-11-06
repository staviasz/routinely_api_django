from unittest.mock import Mock
from main.infra import BaseValidationPydantic
from modules.customer.app import RegisterCustomerController
from modules.customer.contracts import RegisterUsecaseContract
from modules.customer.infra import RegisterCustomerSchema

usecase = Mock(spec=RegisterUsecaseContract)
validor = BaseValidationPydantic(RegisterCustomerSchema)
controller = RegisterCustomerController(usecase=usecase, validator=validor)


class TestRegisterCustomerController:
    def test_no_body_in_request(self):
        response = controller.execute({})

        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "name: Field required",
                "email: Field required",
                "password: Field required",
                "confirmed_password: Field required",
                "accepted_terms: Field required",
            ]
        }

    def test_invalid_data(self):
        response = controller.execute(
            {
                "body": {
                    "name": "in",
                    "email": "invalid",
                    "password": "invalidd",
                    "confirmed_password": "invalidd",
                    "accepted_terms": False,
                }
            }
        )
        print(response)

        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "name: String should have at least 3 characters",
                "email: value is not a valid email address: An email address must have an @-sign.",
                "password: Must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 8 characters long",
                "confirmed_password: Must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 8 characters long",
                "accepted_terms: Terms must be accepted",
            ]
        }

    def test_different_passwords(self):
        response = controller.execute(
            {
                "body": {
                    "name": "valid",
                    "email": "test@test.com",
                    "password": "@Teste123",
                    "confirmed_password": "@Teste1234",
                    "accepted_terms": True,
                }
            }
        )

        assert response["status"] == 400
        print(response)
        assert response["body"] == {"message": ["Passwords: are not equal"]}

    def test_call_usecase(self):
        data = {
            "name": "valid",
            "email": "test@test.com",
            "password": "@Teste123",
            "confirmed_password": "@Teste123",
            "accepted_terms": True,
        }
        controller.execute({"body": data})

        usecase.perform.assert_called_once_with({**data})

    def test_success(self):
        data = {
            "name": "valid",
            "email": "test@test.com",
            "password": "@Teste123",
            "confirmed_password": "@Teste123",
            "accepted_terms": True,
        }
        response = controller.execute({"body": data})

        usecase.perform.assert_called_with({**data})
        assert response["status"] == 204
        assert response["body"] is None
