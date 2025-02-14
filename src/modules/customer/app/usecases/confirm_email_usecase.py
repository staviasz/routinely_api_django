from modules.customer import (
    ConfirmEmailUsecaseContract,
    ConfirmEmailInput,
    ConfirmEmailOutput,
    ConfirmEmailRepositoryContract,
)


class ConfirmEmailUsecase(ConfirmEmailUsecaseContract):
    def __init__(self, repository: ConfirmEmailRepositoryContract) -> None:
        self.repository = repository

    async def perform(self, data: ConfirmEmailInput) -> ConfirmEmailOutput:
        customer = await self.repository.find_field("email", data["email"])
        customer.activate()

        await self.repository.update(customer)
        return
