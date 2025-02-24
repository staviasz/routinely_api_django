from datetime import datetime, timedelta
from typing import get_args

import pytest

from main.errors.shared.custom_error import CustomError
from modules.tasks.domain import TaskEntity, TaskType, TaskCategories


class TestTaskEntity:
    def setup_method(self, method):
        self.data = {
            "user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b",
            "name": "testing",
            "type": "task",
            "category": "productivity",
            "date_time": (datetime.now() + timedelta(hours=1)).strftime(
                "%Y/%m/%d %H:%M:%S"
            ),
            "description": "testing",
            "weekdays": ["monday", "tuesday"],
            "finally_datetime": (datetime.now() + timedelta(days=1)).strftime(
                "%Y/%m/%d %H:%M:%S"
            ),
        }

    def test_validate_entity_type(self):
        str_types = ", ".join(list(get_args(TaskType)))
        arrange = [
            {"data": {**self.data, "type": "invalid"}},
            {"data": {**self.data, "type": ""}},
            {"data": {**self.data, "type": None}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [f"The Type must be one of: {str_types}"],
            }

    def test_validate_entity_name(self):
        arrange = [
            {"data": {**self.data, "name": ""}},
            {"data": {**self.data, "name": " "}},
            {"data": {**self.data, "name": None}},
            {"data": {**self.data, "name": "a" * 51}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [
                    "The name is mandatory and must be up to 50 characters long"
                ],
            }

    def test_validate_entity_date_time_errors(self):
        arrange = [
            {"data": {**self.data, "date_time": ""}},
            {"data": {**self.data, "date_time": None}},
            {"data": {**self.data, "date_time": "wrong_value"}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [
                    "The date_time is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS"
                ],
            }

    def test_validate_entity_date_time_success(self):
        arrange = [
            {
                "data": {**self.data, "date_time": "2021/01/01"},
                "result": "2021-01-01 00:00:00",
            },
            {
                "data": {**self.data, "date_time": "2021/01/01 05:50"},
                "result": "2021-01-01 05:50:00",
            },
            {
                "data": {**self.data, "date_time": "2021/01/01 20:05:50"},
                "result": "2021-01-01 20:05:50",
            },
            {
                "data": {**self.data, "date_time": "2021/01/01T00:35:00"},
                "result": "2021-01-01 00:35:00",
            },
        ]

        for item in arrange:
            entity = TaskEntity(item["data"])
            assert entity.date_time == datetime.fromisoformat(item["result"])

    def test_validate_entity_category(self):
        str_categories = ", ".join(list(get_args(TaskCategories)))
        arrange = [
            {"data": {**self.data, "category": "invalid"}},
            {"data": {**self.data, "category": ""}},
            {"data": {**self.data, "category": None}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [f"The category must be one of: {str_categories}"],
            }

    def test_validate_entity_description(self):
        arrange = [
            {"data": {**self.data, "description": ""}},
            {"data": {**self.data, "description": " "}},
            {"data": {**self.data, "description": None}},
            {"data": {**self.data, "description": "a" * 1001}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [
                    "The Description is mandatory and must be up to 1000 characters long"
                ],
            }

    def test_validate_entity_weekdays(self):
        arrange = [
            {"data": {**self.data, "weekdays": ["invalid"]}},
            {"data": {**self.data, "weekdays": ["monday", "invalid"]}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": ["The Weekdays must be a valid day of the week"],
            }

    def test_validate_entity_finally_date_time_errors(self):
        arrange = [
            {"data": {**self.data, "finally_datetime": "wrong_value"}},
        ]

        for item in arrange:
            with pytest.raises(CustomError) as error:
                TaskEntity(item["data"])

            formate_error = error.value.formate_errors
            assert formate_error == {
                "code_error": 400,
                "messages_error": [
                    "The finally_datetime is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS"
                ],
            }

    def test_entity_errors(self):
        str_types = ", ".join(list(get_args(TaskType)))
        str_categories = ", ".join(list(get_args(TaskCategories)))
        wrong_data = {
            "name": "",
            "type": "invalid",
            "date_time": "",
            "category": "invalid",
            "description": "",
            "weekdays": ["invalid"],
            "finally_datetime": "wrong_value",
        }

        with pytest.raises(CustomError) as error:
            TaskEntity(wrong_data)

        formate_error = error.value.formate_errors
        assert formate_error == {
            "code_error": 400,
            "messages_error": [
                "The user_id in TaskEntity is invalid.",
                f"The Type must be one of: {str_types}",
                f"The category must be one of: {str_categories}",
                "The name is mandatory and must be up to 50 characters long",
                "The date_time is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS",
                "The Description is mandatory and must be up to 1000 characters long",
                "The Weekdays must be a valid day of the week",
                "The finally_datetime is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS",
            ],
        }

    def test_entity_success_with_only_required_fields(self):
        data = self.data.copy()
        del data["weekdays"]
        del data["finally_datetime"]
        entity = TaskEntity(data)

        entity.name == self.data["name"]
        entity.type == self.data["type"]
        entity.date_time == datetime.strptime(
            self.data["date_time"], "%Y/%m/%d %H:%M:%S"
        )
        entity.category == self.data["category"]
        entity.description == self.data["description"]
        entity.weekdays == []
        entity.finally_datetime is None

    def test_entity_success_with_all_fields(self):
        data = self.data.copy()

        entity = TaskEntity(data)

        entity.name == self.data["name"]
        entity.type == self.data["type"]
        entity.date_time == datetime.strptime(
            self.data["date_time"], "%Y/%m/%d %H:%M:%S"
        )
        entity.category == self.data["category"]
        entity.description == self.data["description"]
        entity.weekdays == self.data["weekdays"]
        entity.finally_datetime == datetime.strptime(
            self.data["finally_datetime"], "%Y/%m/%d %H:%M:%S"
        )
