from abc import ABC, abstractmethod
from typing import Generic, Optional, Protocol, TypeVar, Union

from main.domain.aggregates import Aggregate
from main.domain.entity import Entity

T = TypeVar("T", bound=Union[Entity, Aggregate], covariant=True)
K = TypeVar("K", bound=Union[Entity, Aggregate], contravariant=True)

Union_primitive_types = Union[str, int, float, bool, None]


class FindFieldOrNoneContract(Protocol, Generic[T]):
    async def find_field_or_none(
        self, field_name: str, value: Union_primitive_types
    ) -> Optional[T]:
        pass


class FindFieldContract(Protocol, Generic[T]):
    async def find_field(self, field_name: str, value: Union_primitive_types) -> T:
        pass


class DeleteContract(Protocol, Generic[T]):
    async def delete(self, field_name: str, value: Union_primitive_types) -> None:
        pass


class CreateContract(Protocol, Generic[K]):
    async def create(self, aggregate: K) -> None:
        pass
