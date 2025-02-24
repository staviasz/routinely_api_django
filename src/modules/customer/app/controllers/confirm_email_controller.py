from main import (
    BaseController,
    ValidatorContract,
    HttpResponse,
    HttpRequest,
    redirect,
)
from modules.customer import (
    ConfirmEmailUsecaseContract,
    ConfirmEmailSchema,
    EncryptionContract,
)


class ConfirmEmailController(BaseController):
    def __init__(
        self,
        validator: ValidatorContract[ConfirmEmailSchema],
        usecase: ConfirmEmailUsecaseContract,
        crypto: EncryptionContract,
    ) -> None:
        self.validator = validator
        self.usecase = usecase
        self.crypto = crypto

    async def execute(self, request: HttpRequest) -> HttpResponse:
        try:
            query = list((request.get("query") or {}).values())[0]
            query_decrypt_split = self.crypto.decrypt(query).split("--")
            data = {
                "email": query_decrypt_split[0],
                "callback_url": query_decrypt_split[1],
            }

            self.validator.validate(data)
            await self.usecase.perform(self.validator.to_dict())  # type: ignore
            return redirect(data["callback_url"])
        except Exception as e:
            return self._format_response_error(e)
