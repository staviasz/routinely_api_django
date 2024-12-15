from main.app import BaseController, HttpRequest, HttpResponse
from main.app.helpers.http_helpers import no_content
from main.contracts.infra.validator_infra_contract import ValidatorContract
from modules.customer import ConfirmCodeToResetPasswordSchema
from modules.customer.contracts.usecases.confirm_code_to_reset_password_usecase_contract import (
    ConfirmCodeToResetPasswordUsecaseContract,
)


class ConfirmCodeToResetPasswordController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[ConfirmCodeToResetPasswordSchema],
        usecase: ConfirmCodeToResetPasswordUsecaseContract,
    ):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            self.validator.validate(request.get("body") or {})
            await self.usecase.perform(self.validator.to_dict())  # type: ignore
            return no_content()
        except Exception as e:
            return self._format_response_error(e)
