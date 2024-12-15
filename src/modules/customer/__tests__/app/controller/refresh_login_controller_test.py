from unittest.mock import Mock, patch

import pytest
from main.infra.base_validation_pydantic import BaseValidationPydantic
from modules.customer.app.controllers.refresh_login_controller import (
    RefreshLoginController,
)
from modules.customer.contracts.usecases.refresh_login_usecase_contract import (
    RefreshLoginUsecaseContract,
)
from modules.customer.infra.validator.refresh_login_schema import RefreshLoginSchema


@pytest.mark.asyncio
class TestRefreshLoginController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(RefreshLoginSchema)
        self.usecase = Mock(spec=RefreshLoginUsecaseContract)
        self.controller = RefreshLoginController(self.validator, self.usecase)

    async def test_invalid_data(self):
        arrange = [
            {
                "body": {},
                "message": [
                    "access_token: Field required",
                    "refresh_token: Field required",
                ],
            },
            {
                "body": {"access_token": True, "refresh_token": True},
                "message": [
                    "access_token: Input should be a valid string",
                    "refresh_token: Input should be a valid string",
                ],
            },
        ]

        for data in arrange:
            response = await self.controller.execute(data)
            assert response["status"] == 400
            assert response["body"] == {"message": data["message"]}

    async def test_success(self):
        data = {
            "access_token": "any_access_token",
            "refresh_token": "any_refresh_token",
        }

        with patch.object(self.usecase, "perform") as mock_perform:
            self.usecase.perform.return_value = {
                "access_token": "123",
                "refresh_token": "123",
            }

            response = await self.controller.execute({"body": data})

            mock_perform.assert_called_once_with(data)
            assert response["status"] == 200
            assert response["body"] == {
                "access_token": "123",
                "refresh_token": "123",
            }
