from typing import cast
from main.app import BaseController, HttpResponse, HttpRequest, create
from main.contracts import ValidatorContract
from modules.customer.contracts import RegisterUsecaseContract
from modules.customer.infra import RegisterCustomerSchema


class RegisterCustomerController(BaseController):
    def __init__(
        self,
        usecase: RegisterUsecaseContract,
        validator: ValidatorContract[RegisterCustomerSchema],
    ) -> None:
        self.usecase = usecase
        self.validator = validator

    async def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            data = {
                **(request.get("body") or {}),
                "callback_url": (request.get("query") or {}).get("callback_url"),
            }
            self.validator.validate(data)
            await self.usecase.perform(self.validator.to_dict())  # type: ignore
            return create({})
        except Exception as e:
            return self._format_response_error(e)
