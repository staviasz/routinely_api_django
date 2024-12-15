from unittest.mock import Mock, patch

import pytest
from main.infra.base_validation_pydantic import BaseValidationPydantic
from modules.customer.app.controllers.new_password_controller import (
    NewPasswordController,
)
from modules.customer.contracts.usecases.new_password_usecase_contract import (
    NewPasswordUsecaseContract,
)
from modules.customer.infra.validator.new_password_schema import NewPasswordValidator


@pytest.mark.asyncio
class TestNewPasswordController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(NewPasswordValidator)
        self.usecase = Mock(spec=NewPasswordUsecaseContract)
        self.controller = NewPasswordController(self.validator, self.usecase)

    async def test_invalid_request(self):
        arrange = [
            {
                "body": {},
                "message": [
                    "account_id: Field required",
                    "password: Field required",
                    "confirm_password: Field required",
                ],
            },
            {
                "body": {
                    "account_id": 123,
                    "password": "any_password",
                    "confirm_password": "any_confirm_password",
                },
                "message": [
                    "account_id: Input should be a valid string",
                    "password: The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
                    "confirm_password: The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
                ],
            },
            {
                "body": {
                    "account_id": "any_account_id",
                    "password": "@Test123",
                    "confirm_password": "@Test12",
                },
                "message": ["The confirm password must match the password."],
            },
        ]

        for data in arrange:
            response = await self.controller.execute(data)
            assert response["status"] == 400
            assert response["body"] == {"message": data["message"]}

    async def test_success(self):
        data = {
            "account_id": "any_account_id",
            "password": "@Test123",
            "confirm_password": "@Test123",
        }

        with patch.object(self.usecase, "perform") as mock_perform:

            response = await self.controller.execute({"body": data})

            mock_perform.assert_called_once_with(data)
            assert response["status"] == 204
            assert response["body"] is None
