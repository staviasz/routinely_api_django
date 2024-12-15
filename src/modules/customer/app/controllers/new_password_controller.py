from main.app import BaseController, HttpRequest, HttpResponse, no_content
from main.contracts.infra.validator_infra_contract import ValidatorContract
from modules.customer import NewPasswordUsecaseContract, NewPasswordValidator


class NewPasswordController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[NewPasswordValidator],
        usecase: NewPasswordUsecaseContract,
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
