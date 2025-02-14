from modules.auth.contracts.services.session_service_contract import (
    SessionServiceContract,
)
from modules.customer.contracts import RefreshLoginUsecaseContract
from modules.customer.types.refresh_login_dto import (
    RefreshLoginInput,
    RefreshLoginOutput,
)


class RefreshLoginUsecase(RefreshLoginUsecaseContract):
    def __init__(self, auth: SessionServiceContract) -> None:
        self.auth = auth

    async def perform(self, data: RefreshLoginInput) -> RefreshLoginOutput:
        print(data)
        return await self.auth.handle({"tokens": data})
