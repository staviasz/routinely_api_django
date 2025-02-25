import pytest
from unittest.mock import Mock, patch

from main import BaseValidationPydantic
from modules.tasks import ListTasksSchema, ListTasksUsecaseContract, ListTaskController


@pytest.mark.asyncio
class TestListTaskController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(ListTasksSchema)
        self.usecase = Mock(spec=ListTasksUsecaseContract)
        self.controller = ListTaskController(self.validator, self.usecase)
        self.user_id = "user_id_test"
        self.data = {"month": 1, "year": 2023}

    async def test_execute_validate_user_id(self):
        arrange = [
            {
                "session": {"user_id": ""},
                "message": ["user_id: String should have at least 1 character"],
            },
            {
                "session": {"user_id": 1},
                "message": ["user_id: Input should be a valid string"],
            },
            {
                "session": {"user_id": True},
                "message": ["user_id: Input should be a valid string"],
            },
            {"session": {}, "message": ["user_id: Input should be a valid string"]},
        ]

        for item in arrange:
            response = await self.controller.execute({"session": item["session"]})
            assert response["status"] == 400
            assert response["body"] == {
                "message": item["message"],
            }

    async def test_execute_validate_month(self):
        arrange = [
            {
                "body": {"month": 0},
                "message": ["month: Input should be greater than or equal to 1"],
            },
            {
                "body": {"month": 13},
                "message": ["month: Input should be less than or equal to 12"],
            },
            {
                "body": {"month": "test"},
                "message": ["month: Input should be a valid integer"],
            },
            {
                "body": {"month": True},
                "message": ["month: Input should be a valid integer"],
            },
        ]

        for item in arrange:
            response = await self.controller.execute(
                {"session": {"user_id": self.user_id}, "body": item["body"]}
            )
            assert response["status"] == 400
            assert response["body"] == {
                "message": item["message"],
            }

    async def test_execute_validate_year(self):
        arrange = [
            {
                "body": {"year": 1999},
                "message": ["year: Input should be greater than or equal to 2000"],
            },
            {
                "body": {"year": "test"},
                "message": ["year: Input should be a valid integer"],
            },
            {
                "body": {"year": True},
                "message": ["year: Input should be a valid integer"],
            },
        ]

        for item in arrange:
            response = await self.controller.execute(
                {"session": {"user_id": self.user_id}, "body": item["body"]}
            )
            assert response["status"] == 400
            assert response["body"] == {
                "message": item["message"],
            }

    async def test_execute_error_usecase(self):
        self.usecase.perform.side_effect = Exception("error")
        response = await self.controller.execute(
            {"session": {"user_id": self.user_id}, "body": self.data}
        )
        assert response["status"] == 500
        assert response["body"] == {"message": ["Internal Server Error"]}

    async def test_execute_success(self):
        with patch.object(self.usecase, "perform") as mock:
            self.usecase.perform.return_value = {"tasks": []}
            response = await self.controller.execute(
                {"session": {"user_id": self.user_id}, "body": self.data}
            )
            assert response["status"] == 200
            assert response["body"] == {"tasks": []}
        mock.assert_called_once_with({**self.data, "user_id": self.user_id})
