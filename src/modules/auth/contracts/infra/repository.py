from datetime import datetime
from typing import Generic, Protocol, TypeVar
from main.contracts import CreateContract, FindFieldOrNoneContract, DeleteContract
from modules.auth.domain import SessionEntity

E = TypeVar("E", bound=SessionEntity, covariant=True)
T = SessionEntity


class FindSessionContract(Protocol, Generic[E]):
    async def find_session_or_none(self, user_id: str) -> E | None:
        pass


class CreateSessionRepositoryContract(CreateContract[T], FindSessionContract[T]):
    pass


class SessionRepositoryContract(CreateSessionRepositoryContract):
    pass
