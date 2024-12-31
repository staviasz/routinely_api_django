from main import ValidatorContract, create, BaseController
from modules.tasks import CreateTaskUsecaseContract, CreateTaskSchema


class CreateTaskController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[CreateTaskSchema],
        usecase: CreateTaskUsecaseContract,
    ):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request):
        try:
            self.validator.validate(request.get("body") or {})
            response = await self.usecase.perform(self.validator.to_dict())  # type: ignore
            return create({**response})
        except Exception as e:
            return self._format_response_error(e)
