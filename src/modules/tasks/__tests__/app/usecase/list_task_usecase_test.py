# flake8: noqa: W503

import copy
from datetime import datetime
from typing import TypedDict
from unittest.mock import patch
import pytest
from modules.tasks.app.usecases.list_task_usecase import ListTaskUsecase
from modules.tasks.types.list_tasks_dto import TaskModel


class FakeEntityProps(TypedDict, TaskModel):
    user_id: str


class FakeEntity:
    def __init__(self, props: FakeEntityProps) -> None:
        self.props = props

    def to_dict(self) -> FakeEntityProps:
        return {
            "id": self.props["id"],
            "user_id": self.props["user_id"],
            "category": self.props["category"],
            "name": self.props["name"],
            "type": self.props["type"],
            "date_time": self.props["date_time"],
            "description": self.props["description"],
            "weekdays": self.props["weekdays"],
            "finally_datetime": self.props["finally_datetime"],
        }


class ListTaskRepositoryInMemory:
    list_data: list = []

    async def find_tasks_by_user_id_and_month_and_year(self, user_id, month, year):
        items = []

        for item in self.list_data:
            item_dict = item.to_dict()
            date = datetime.strptime(item_dict["date_time"], "%Y/%m/%d")
            if (
                item_dict["user_id"] == user_id
                and date.month == month
                and date.year == year
            ):
                items.append(item)

        return items


@pytest.mark.asyncio
class TestListTaskUsecase:
    def setup_method(self):
        self.repository = ListTaskRepositoryInMemory()
        self.usecase = ListTaskUsecase(self.repository)

    async def test_perform_with_default_month_and_year(self):
        now = datetime.now()
        month = now.month
        year = now.year

        with patch.object(
            self.repository, "find_tasks_by_user_id_and_month_and_year"
        ) as mock:
            await self.usecase.perform({"user_id": "user_id"})

        mock.assert_awaited_once_with("user_id", month, year)

    async def test_perform_with_custom_month_and_year(self):
        with patch.object(
            self.repository, "find_tasks_by_user_id_and_month_and_year"
        ) as mock:
            await self.usecase.perform({"user_id": "user_id", "month": 1, "year": 2023})

        mock.assert_awaited_once_with("user_id", 1, 2023)

    async def test_perform_return_correct_filter(self):
        data = [
            {
                "user_id": "user_id",
                "category": "category",
                "name": "name",
                "id": "id",
                "type": "type",
                "date_time": "2024/05/01",
                "description": "description",
                "weekdays": "weekdays",
                "finally_datetime": "2023/01/01",
            },
            {
                "user_id": "user_id",
                "category": "category",
                "name": "name",
                "id": "id",
                "type": "type",
                "date_time": "2023/01/01",
                "description": "description",
                "weekdays": "weekdays",
                "finally_datetime": "2023/01/01",
            },
            {
                "user_id": "user_id",
                "category": "category",
                "name": "name",
                "id": "id",
                "type": "type",
                "date_time": "2023/01/01",
                "description": "description",
                "weekdays": "weekdays",
                "finally_datetime": "2023/01/01",
            },
        ]

        for item in data:
            self.repository.list_data.append(FakeEntity(item))

        arrange = [
            {"user_id": "user_id", "expected": []},
            {"user_id": "user_id2", "month": 1, "year": 2023, "expected": []},
            {"user_id": "user_id", "month": 1, "year": 2023, "expected": data[1:3]},
            {"user_id": "user_id", "month": 5, "year": 2024, "expected": [data[0]]},
        ]

        for item in arrange:
            result = await self.usecase.perform(item)
            print("result", result)
            print("expected", item["expected"])

            expect = []
            for task in item["expected"]:
                copy_task = copy.deepcopy(task)
                del copy_task["user_id"]
                expect.append(copy_task)

            assert result["tasks"] == expect
