from typing import cast
from unittest.mock import Mock

import pytest
from main.app.controller.base_controller import BaseController
from main.app.helpers.http_helpers import create, no_content, ok
from main.app.types.http_types import HttpResponse, HttpRequest
from main.errors.shared.custom_error import CustomError, CustomErrorAbstract


class ConcreteError(CustomErrorAbstract):
    def __init__(self, code_error: int, message_error: str):
        super().__init__(code_error=code_error, message_error=message_error)


class ConcreteControllerBase(BaseController):

    def __init__(self, usecase):
        self.usecase = usecase

    async def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            result: HttpResponse = self.usecase()

            match result["status"]:
                case 200:
                    return ok(cast(dict, result["body"]))
                case 201:
                    return create(cast(dict, result["body"]))
                case 204:
                    return no_content()

            if 500 >= result["status"] > 299:
                raise CustomError(
                    ConcreteError(
                        code_error=result["status"],
                        message_error=(
                            result["body"]["message"] if result["body"] else ""
                        ),
                    )
                )
            raise Exception("error")
        except Exception as e:
            return self._format_response_error(e)


@pytest.mark.asyncio
class TestControllerBase:
    def setup_method(self):
        self.usecase = Mock()
        self.request = {"body": {"name": "Teste"}}
        self.controller = ConcreteControllerBase(self.usecase)

    async def test_execute_success(self):

        arrange = [
            {"status": 200, "body": {"name": "success"}},
            {"status": 201, "body": {"name": "created"}},
            {"status": 204, "body": None},
        ]
        for response in arrange:
            self.usecase.return_value = response
            result = await self.controller.execute(self.request)
            print("result", result["body"], "response", response["body"])
            assert result["status"] == response["status"]
            assert result["body"] == response["body"]

    async def test_execute_error(self):
        arrange = [
            {"status": 401, "body": {"message": "unauthorized"}},
            {"status": 400, "body": {"message": "bad request"}},
            {"status": 403, "body": {"message": "forbidden"}},
            {"status": 404, "body": {"message": "not found"}},
            {"status": 409, "body": {"message": "conflict"}},
            {"status": 500, "body": {"message": "Internal Server Error"}},
        ]

        for response in arrange:
            self.usecase.return_value = response
            result = await self.controller.execute(self.request)
            assert result["status"] == response["status"]
            assert result["body"]["message"] == [response["body"]["message"]]

    async def test_execute_exception_default(self):
        arrange = {
            "status": 501,
            "body": {"message": "error"},
        }
        self.usecase.return_value = arrange
        result = await self.controller.execute(self.request)
        assert result["status"] == 500
        assert result["body"]["message"] == ["Internal Server Error"]
