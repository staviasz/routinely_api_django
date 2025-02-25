from unittest.mock import Mock, patch

import pytest
from main import BaseValidationPydantic
from modules.tasks import (
    DeleteTaskSchema,
    DeleteTaskUsecaseContract,
    DeleteTaskController,
)


@pytest.mark.asyncio
class TestDeleteTaskController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(DeleteTaskSchema)
        self.usecase = Mock(spec=DeleteTaskUsecaseContract)
        self.controller = DeleteTaskController(self.validator, self.usecase)

    async def test_execute_validate_params(self):
        arrange = [
            {"params": {}, "message": ["id: Field required"]},
            {"params": {"id": 1}, "message": ["id: Input should be a valid string"]},
            {"params": {"id": True}, "message": ["id: Input should be a valid string"]},
        ]

        for item in arrange:
            response = await self.controller.execute({"params": item["params"]})
            assert response["status"] == 400
            assert response["body"] == {
                "message": item["message"],
            }

    async def test_execute_return_error_usecase(self):
        self.usecase.perform.side_effect = Exception("test")
        response = await self.controller.execute({"params": {"id": "test"}})
        assert response["status"] == 500
        assert response["body"] == {"message": ["Internal Server Error"]}

    async def test_execute_return_success(self):
        with patch.object(
            self.usecase,
            "perform",
        ) as mock:
            self.usecase.perform.return_value = None
            response = await self.controller.execute({"params": {"id": "test"}})
            assert response["status"] == 204
            assert response["body"] is None
        mock.assert_called_once_with({"id": "test"})
