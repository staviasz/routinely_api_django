from main.errors.shared.bad_request_error import BadRequestError
from main.errors.shared.custom_error import CustomError
from modules.customer.contracts import (
    ConfirmCodeToResetPasswordUsecaseContract,
    ConfirmCodeToResetPasswordRepositoryContract,
)
from modules.customer.infra.cache.cache import Cache
from modules.customer.types import ConfirmCodeToResetPasswordInput


class ConfirmCodeToResetPasswordUsecase(ConfirmCodeToResetPasswordUsecaseContract):
    def __init__(
        self,
        repository: ConfirmCodeToResetPasswordRepositoryContract,
        cache: Cache,
    ) -> None:
        self.cache = cache
        self.repository = repository

    async def perform(self, data: ConfirmCodeToResetPasswordInput) -> None:
        customer = await self.repository.find_field("id", data["id"])
        code = self.cache.get(customer.email)

        if not code:
            raise CustomError(BadRequestError("Expired code."))

        if code != data["code"]:
            raise CustomError(BadRequestError("Invalid code."))

        customer.activate()

        await self.repository.update(customer)
