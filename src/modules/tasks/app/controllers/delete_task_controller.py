from main import BaseController, ValidatorContract, no_content
from modules.tasks import DeleteTaskUsecaseContract, DeleteTaskSchema


class DeleteTaskController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[DeleteTaskSchema],
        usecase: DeleteTaskUsecaseContract,
    ):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request):
        try:
            self.validator.validate(request.get("params") or {})
            await self.usecase.perform(self.validator.to_dict())
            return no_content()
        except Exception as e:
            return self._format_response_error(e)
