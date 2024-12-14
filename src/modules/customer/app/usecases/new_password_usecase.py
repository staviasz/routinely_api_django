from main.errors.shared.bad_request_error import BadRequestError
from main.errors.shared.custom_error import CustomError
from modules.customer.contracts import (
    NewPasswordRepositoryContract,
    NewPasswordUsecaseContract,
)
from modules.customer.types import NewPasswordOutput, NewPasswordInput


class NewPasswordUsecase(NewPasswordUsecaseContract):
    def __init__(self, repository: NewPasswordRepositoryContract):
        self.repository = repository

    async def perform(self, data: NewPasswordInput) -> NewPasswordOutput:

        if data["password"] != data["confirm_password"]:
            raise CustomError(BadRequestError("Passwords do not match."))

        customer = await self.repository.find_field("id", data["account_id"])

        customer.change_password(data["password"])

        await self.repository.update(customer)

        return
