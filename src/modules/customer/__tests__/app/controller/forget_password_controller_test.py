from unittest.mock import Mock, patch

import pytest
from main.infra import BaseValidationPydantic
from modules.customer import (
    ForgetPasswordController,
    ForgetPasswordUsecaseContract,
    ForgetPasswordSchema,
)


@pytest.mark.asyncio
class TestForgetPasswordController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(ForgetPasswordSchema)
        self.usecase = Mock(spec=ForgetPasswordUsecaseContract)
        self.controller = ForgetPasswordController(self.validator, self.usecase)

    async def test_validate_data(self):
        arrange = [
            {
                "body": {"email": "email"},
                "message": [
                    "email: value is not a valid email address: An email address must have an @-sign."
                ],
            },
            {
                "body": {"email": "test@example"},
                "message": [
                    "email: value is not a valid email address: The part after the @-sign is not valid. It should have a period."
                ],
            },
            {
                "body": {"email": "test@.com"},
                "message": [
                    "email: value is not a valid email address: An email address cannot have a period immediately after the @-sign."
                ],
            },
        ]

        for data in arrange:
            response = await self.controller.execute(data)
            assert response["status"] == 400
            assert response["body"] == {"message": data["message"]}

    async def test_success(self):
        with patch.object(self.usecase, "perform") as mock_perform:
            self.usecase.perform.return_value = {"account_id": "123"}
            response = await self.controller.execute(
                {"body": {"email": "G0s7B@example.com"}}
            )
            mock_perform.assert_called_once_with({"email": "G0s7B@example.com"})

        assert response["status"] == 200
        assert response["body"] == {"account_id": "123"}
