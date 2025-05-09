from typing import (
    Awaitable,
    Generic,
    Optional,
    Protocol,
    TypeVar,
    TypedDict,
    Union,
)


class OBJ(TypedDict):
    pass


Input = Union[OBJ, dict, str, None]

Output = Awaitable[Optional[Input]] | Optional[Input]

T = TypeVar("T", bound=Input)
U = TypeVar("U", bound=Output, covariant=True)


class BaseServiceContract(Protocol, Generic[T, U]):
    async def handle(self, data: T) -> U:
        pass

    async def verify_token(self, token: str) -> T:
        pass
