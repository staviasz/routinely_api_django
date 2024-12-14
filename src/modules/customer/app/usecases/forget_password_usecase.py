import random
from main.contracts import EventBaseClass, DispatcherContract
from modules.customer.contracts import (
    ForgetPasswordUsecaseContract,
    ForgetPasswordRepositoryContract,
)
from modules.customer.infra import CacheForgetPasswordCode
from modules.customer.types import ForgetPasswordInput, ForgetPasswordOutput


class ForgetPasswordUsecase(ForgetPasswordUsecaseContract):

    def __init__(
        self,
        repository: ForgetPasswordRepositoryContract,
        cache: CacheForgetPasswordCode,
        event: EventBaseClass,
        dispatcher: DispatcherContract,
    ) -> None:
        self.repository = repository
        self.cache = cache
        self.event = event
        self.dispatcher = dispatcher

    async def perform(self, data: ForgetPasswordInput) -> ForgetPasswordOutput:

        customer = await self.repository.find_field("email", data["email"])

        code = str(random.randint(100000, 999999))

        self.cache.set(customer.email, code)

        self.event.set_payload(
            {"name": customer.name, "email": customer.email, "code": code}
        )
        self.dispatcher.dispatch(self.event)

        return {"account_id": customer.id}
