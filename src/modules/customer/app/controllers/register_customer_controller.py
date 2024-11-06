from typing import cast
from main.app import BaseController, no_content, HttpResponse, HttpRequest
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

    def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            self.validator.validate(request.get("body") or {})
            self.usecase.perform(self.validator.to_dict())  # type: ignore
            return no_content()
        except Exception as e:
            return self._format_response_error(e)
