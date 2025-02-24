from abc import ABC, abstractmethod
from typing import Coroutine

from main.app import (
    HttpResponse,
    HttpRequest,
    internal_server_error,
    bad_request,
    unauthorized,
    forbidden,
    not_found,
    conflict,
)
from main.errors import CustomError


class BaseController(ABC):
    @abstractmethod
    async def execute(self, request: HttpRequest) -> HttpResponse:
        pass

    def _format_response_error(self, error: Exception) -> HttpResponse:
        if not isinstance(error, CustomError):
            return internal_server_error()

        match error.formate_errors["code_error"]:
            case 400:
                return bad_request(error)
            case 401:
                return unauthorized(error)
            case 403:
                return forbidden(error)
            case 404:
                return not_found(error)
            case 409:
                return conflict(error)
            case _:
                return internal_server_error()
