from abc import ABC, abstractmethod
from typing import Any, Awaitable, Generic, Optional, TypeVar, TypedDict, Union


class OBJ(TypedDict):
    pass


Input = Union[OBJ, str, None]

Output = Union[Awaitable[Optional[Input]], Optional[Input]]

T = TypeVar("T", bound=Input)


class BaseUsecaseContract(ABC, Generic[T]):
    @abstractmethod
    def perform(self, data: T) -> Output:
        pass
