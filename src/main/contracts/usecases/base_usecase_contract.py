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


Input = Union[OBJ, str, None]

Output = Union[Awaitable[Optional[Input]], Optional[Input]]

T = TypeVar("T", bound=Input, contravariant=True)
U = TypeVar("U", bound=Output, covariant=True)


class BaseUsecaseContract(Protocol, Generic[T, U]):
    async def perform(self, data: T) -> U:
        pass
