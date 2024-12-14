from typing import Any, cast
from main.errors.shared.custom_error import CustomError
from modules.auth.contracts import SessionServiceContract
from modules.customer.app import UnauthorizedError
from modules.customer.types import LoginInput, LoginOutput
from modules.customer.contracts import (
    LoginUsecaseContract,
    LoginRepositoryContract,
)


class LoginUsecase(LoginUsecaseContract):
    def __init__(
        self,
        repository: LoginRepositoryContract,
        auth: SessionServiceContract,
    ) -> None:
        self.repository = repository
        self.auth = auth
        self.hash = hash

    async def perform(self, data: LoginInput) -> LoginOutput:

        user = await self.repository.find_field("email", data["email"])

        if data["password"] != user.password:
            raise CustomError(UnauthorizedError("Invalid credentials"))

        payload = cast(Any, {"id": user.id, "email": user.email})
        return await self.auth.handle(payload)
