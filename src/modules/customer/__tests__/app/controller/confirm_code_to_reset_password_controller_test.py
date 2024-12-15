from unittest.mock import Mock, patch

import pytest
from main.infra import BaseValidationPydantic
from modules.customer import (
    ConfirmCodeToResetPasswordSchema,
    ConfirmCodeToResetPasswordUsecaseContract,
)
from modules.customer.app.controllers.confirm_code_to_reset_password_controller import (
    ConfirmCodeToResetPasswordController,
)


@pytest.mark.asyncio
class TestConfirmCodeToResetPasswordController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(ConfirmCodeToResetPasswordSchema)
        self.usecase = Mock(spec=ConfirmCodeToResetPasswordUsecaseContract)
        self.controller = ConfirmCodeToResetPasswordController(
            self.validator, self.usecase
        )

    async def test_validate_empty_body(self):
        response = await self.controller.execute({"body": {}})
        assert response["status"] == 400
        assert response["body"] == {
            "message": ["code: Field required", "email: Field required"]
        }

    async def test_invalid_data(self):
        response = await self.controller.execute(
            {"body": {"email": "invalid", "code": "code__"}}
        )
        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "code: Code must be a number",
                "email: value is not a valid email address: An email address must have an @-sign.",
            ]
        }

    async def test_success(self):
        with patch.object(self.usecase, "perform") as mock_perform:
            response = await self.controller.execute(
                {"body": {"email": "G0s7B@example.com", "code": "123456"}}
            )
            mock_perform.assert_called_once_with(
                {"email": "G0s7B@example.com", "code": "123456"}
            )
        assert response["status"] == 204
        assert response["body"] is None