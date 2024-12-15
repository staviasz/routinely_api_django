from main.app import BaseController, HttpRequest, HttpResponse, ok
from main.contracts.infra.validator_infra_contract import ValidatorContract
from modules.customer import ForgetPasswordSchema, ForgetPasswordUsecaseContract


class ForgetPasswordController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[ForgetPasswordSchema],
        usecase: ForgetPasswordUsecaseContract,
    ):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            self.validator.validate(request.get("body") or {})
            response = await self.usecase.perform(self.validator.to_dict())  # type: ignore
            return ok({**response})
        except Exception as e:
            return self._format_response_error(e)
