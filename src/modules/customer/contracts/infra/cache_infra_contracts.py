from typing import Protocol, TypeVar, Generic

T = TypeVar("T")


class CacheContract(Protocol, Generic[T]):
    def get(self, key: str) -> T:
        pass

    def set(self, key: str, value: T) -> None:
        pass
