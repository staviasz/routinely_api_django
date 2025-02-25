from main import BaseController, ValidatorContract, ok
from modules.tasks import ListTasksUsecaseContract


class ListTaskController(BaseController):
    def __init__(self, validator: ValidatorContract, usecase: ListTasksUsecaseContract):
        self.validator = validator
        self.usecase = usecase

    async def execute(self, request):
        try:
            user_id = request.get("session").get("user_id")
            body = request.get("body")
            data = {
                "user_id": user_id,
                "month": body.get("month") if body else None,
                "year": body.get("year") if body else None,
            }
            self.validator.validate(data)
            response = await self.usecase.perform(self.validator.to_dict())

            return ok({**response})
        except Exception as e:
            return self._format_response_error(e)
