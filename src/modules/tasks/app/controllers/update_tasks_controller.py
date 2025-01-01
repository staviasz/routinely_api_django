from main import BaseController, ValidatorContract, no_content
from modules.tasks import UpdateTaskUsecaseContract


class UpdateTaskController(BaseController):
    def __init__(
        self, validator: ValidatorContract, usecase: UpdateTaskUsecaseContract
    ):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request):
        try:
            user_id = request.get("headers").get("user_id")
            body = request.get("body", {})
            data = {"user_id": user_id, **body}
            print(data)

            self.validator.validate(data)
            await self.usecase.perform(self.validator.to_dict())
            return no_content()
        except Exception as e:
            return self._format_response_error(e)
