import copy
from datetime import datetime, timedelta
from typing import get_args
import pytest
from unittest.mock import Mock, patch

from main import BaseValidationPydantic
from modules.tasks import (
    CreateTaskController,
    CreateTaskUsecaseContract,
    CreateTaskSchema,
    TaskType,
    TaskCategories,
    Weekday,
)


def formate_types_in_str(types: list[str]) -> str:
    len_types = len(types)
    if len_types == 1:
        return f"'{types[0]}'"

    if len_types == 2:
        return f"'{types[0]}' or '{types[1]}'"

    return f"{', '.join(f"'{t}'" for t in types[:-1])} or '{types[-1]}'"


@pytest.mark.asyncio
class TestCreateTaskController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(CreateTaskSchema)
        self.usecase = Mock(spec=CreateTaskUsecaseContract)
        self.controller = CreateTaskController(self.validator, self.usecase)
        self.user_id = "user_id_test"
        now = datetime.now()
        self.data = {
            "description": "description_test",
            "category": "career",
            "name": "name_test_",
            "type": "task",
            "date_time": (now + timedelta(minutes=10)).strftime("%Y/%m/%d %H:%M"),
            "weekdays": ["monday", "tuesday"],
            "finally_datetime": (now + timedelta(days=1)).strftime("%Y/%m/%d %H:%M"),
        }

    async def test_execute_return_errors_if_body_is_empty(self):
        response = await self.controller.execute({"session": {}})
        assert response["status"] == 400
        assert response["body"] == {
            "message": [
                "user_id: Input should be a valid string",
                "description: Field required",
                "category: Field required",
                "name: Field required",
                "type: Field required",
                "date_time: Field required",
            ]
        }

    async def test_execute_validate_field_user_id(self):
        arrange = [
            {
                "session": {"user_id": 1},
                "message": ["user_id: Input should be a valid string"],
            },
            {
                "session": {"user_id": True},
                "message": ["user_id: Input should be a valid string"],
            },
            {
                "session": {},
                "message": ["user_id: Input should be a valid string"],
            },
        ]

        for item in arrange:
            response = await self.controller.execute(
                {
                    "session": item["session"],
                    "body": self.data,
                }
            )
            assert response["status"] == 400
            assert response["body"] == {
                "message": item["message"],
            }

    async def test_execute_validate_field_description(self):
        new_data = copy.deepcopy(self.data)
        del new_data["description"]
        arrange = [
            {
                "body": {**new_data, "description": 1},
                "message": ["description: Input should be a valid string"],
            },
            {
                "body": {**new_data, "description": True},
                "message": ["description: Input should be a valid string"],
            },
            {
                "body": new_data,
                "message": ["description: Field required"],
            },
            {
                "body": {**new_data, "description": "a" * 1001},
                "message": ["description: String should have at most 1000 characters"],
            },
            {
                "body": {**new_data, "description": " "},
                "message": ["description: String should have at least 10 characters"],
            },
            {
                "body": {**new_data, "description": "a" * 5},
                "message": ["description: String should have at least 10 characters"],
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

    async def test_execute_validate_field_category(self):
        new_data = copy.deepcopy(self.data)
        del new_data["category"]

        arrange = [
            {
                "body": {**new_data, "category": 1},
                "message": [
                    f"category: Input should be {formate_types_in_str(list(get_args(TaskCategories)))}"
                ],
            },
            {
                "body": {**new_data, "category": "test"},
                "message": [
                    f"category: Input should be {formate_types_in_str(list(get_args(TaskCategories)))}"
                ],
            },
            {
                "body": new_data,
                "message": ["category: Field required"],
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

    async def test_execute_validate_field_name(self):
        new_data = copy.deepcopy(self.data)
        del new_data["name"]
        arrange = [
            {
                "body": {**new_data, "name": 1},
                "message": ["name: Input should be a valid string"],
            },
            {
                "body": {**new_data, "name": True},
                "message": ["name: Input should be a valid string"],
            },
            {
                "body": new_data,
                "message": ["name: Field required"],
            },
            {
                "body": {**new_data, "name": "a" * 51},
                "message": ["name: String should have at most 50 characters"],
            },
            {
                "body": {**new_data, "name": " "},
                "message": ["name: String should have at least 10 characters"],
            },
            {
                "body": {**new_data, "name": "a" * 5},
                "message": ["name: String should have at least 10 characters"],
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

    async def test_execute_validate_field_type(self):
        new_data = copy.deepcopy(self.data)
        del new_data["type"]
        arrange = [
            {
                "body": {**new_data, "type": 1},
                "message": [
                    f"type: Input should be {formate_types_in_str(list(get_args(TaskType)))}"
                ],
            },
            {
                "body": {**new_data, "type": "test"},
                "message": [
                    f"type: Input should be {formate_types_in_str(list(get_args(TaskType)))}"
                ],
            },
            {
                "body": new_data,
                "message": ["type: Field required"],
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

    async def test_execute_validate_field_date_time(self):
        new_data = copy.deepcopy(self.data)
        del new_data["date_time"]
        arrange = [
            {
                "body": {**new_data, "date_time": 1},
                "message": ["date_time: Input should be a valid string"],
            },
            {
                "body": {**new_data, "date_time": True},
                "message": ["date_time: Input should be a valid string"],
            },
            {
                "body": new_data,
                "message": ["date_time: Field required"],
            },
            {
                "body": {**new_data, "date_time": "test"},
                "message": [
                    "date_time: Invalid date format, expected formats YYYY/MM/DD, YYYY/MM/DD HH:MM, YYYY/MM/DD HH:MM:SS, YYYY/MM/DDTHH:MM:SS"
                ],
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

    async def test_execute_validate_field_weekdays(self):
        new_data = copy.deepcopy(self.data)
        del new_data["weekdays"]
        arrange = [
            {
                "body": {**new_data, "weekdays": 1},
                "message": ["weekdays: Input should be a valid list"],
            },
            {
                "body": {**new_data, "weekdays": True},
                "message": ["weekdays: Input should be a valid list"],
            },
            {
                "body": {**new_data, "weekdays": "test"},
                "message": ["weekdays: Input should be a valid list"],
            },
            {
                "body": {**new_data, "weekdays": ["test"]},
                "message": [
                    f"weekdays: Input should be {formate_types_in_str(list(get_args(Weekday)))}"
                ],
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

    async def test_execute_validate_field_finally_date(self):
        new_data = copy.deepcopy(self.data)
        del new_data["finally_datetime"]
        arrange = [
            {
                "body": {**new_data, "finally_datetime": 1},
                "message": ["finally_datetime: Input should be a valid string"],
            },
            {
                "body": {**new_data, "finally_datetime": True},
                "message": ["finally_datetime: Input should be a valid string"],
            },
            {
                "body": {**new_data, "finally_datetime": "test"},
                "message": [
                    "finally_datetime: Invalid date format, expected formats YYYY/MM/DD, YYYY/MM/DD HH:MM, YYYY/MM/DD HH:MM:SS, YYYY/MM/DDTHH:MM:SS"
                ],
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

    async def test_execute_return_error_to_usecase(self):
        self.usecase.perform.side_effect = Exception("test")
        response = await self.controller.execute({"body": self.data})
        assert response["status"] == 500
        assert response["body"] == {"message": ["Internal Server Error"]}

    async def test_execute_return_success(self):

        with patch.object(
            self.usecase,
            "perform",
        ) as mock:
            self.usecase.perform.return_value = {"id": "any_id"}

            response = await self.controller.execute(
                {"session": {"user_id": self.user_id}, "body": self.data}
            )
            assert response["status"] == 201
            assert response["body"] == {
                "id": "any_id",
            }
        mock.assert_called_once_with({**self.data, "user_id": self.user_id})
