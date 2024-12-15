from unittest.mock import Mock, patch

import pytest
from main.infra.base_validation_pydantic import BaseValidationPydantic
from modules.customer.app.controllers.login_controller import LoginController
from modules.customer.contracts.usecases.login_usecase_contract import (
    LoginUsecaseContract,
)
from modules.customer.infra.validator.login_customer_schema import LoginValidator


@pytest.mark.asyncio
class TestLoginController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(LoginValidator)
        self.usecase = Mock(spec=LoginUsecaseContract)
        self.controller = LoginController(self.validator, self.usecase)

    async def test_invalid_data(self):
        arrange = [
            {
                "body": {},
                "message": ["email: Field required", "password: Field required"],
            },
            {
                "body": {
                    "email": "invalid",
                    "password": "password",
                    "remember_me": "any_value",
                },
                "message": [
                    "email: value is not a valid email address: An email address must have an @-sign.",
                    "password: The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
                    "remember_me: Input should be a valid boolean, unable to interpret input",
                ],
            },
        ]

        for data in arrange:
            response = await self.controller.execute(data)
            assert response["status"] == 400
            assert response["body"] == {"message": data["message"]}

    async def test_success(self):
        body_req = {"email": "G0s7B@example.com", "password": "@Teste123"}
        with patch.object(self.usecase, "perform") as mock_perform:
            self.usecase.perform.return_value = {
                "access_token": "123",
                "refresh_token": "123",
                "expires_in": 3600,
            }

            response = await self.controller.execute({"body": body_req})
            mock_perform.assert_called_once_with(
                {
                    **body_req,
                    "remember_me": False,
                }
            )

        assert response["status"] == 200
        assert response["body"] == {
            "access_token": "123",
            "refresh_token": "123",
            "expires_in": 3600,
        }
