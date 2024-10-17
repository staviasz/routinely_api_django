from abc import ABC, abstractmethod
from typing import Generic, Optional, Protocol, TypeVar, Union

from main.domain.aggregates import Aggregate
from main.domain.entity import Entity

T = TypeVar("T", bound=Union[Entity, Aggregate], covariant=True)
K = TypeVar("K", bound=Union[Entity, Aggregate], contravariant=True)

Union_primitive_types = Union[str, int, float, bool, None]


class FindFieldOrNoneContract(Protocol, Generic[T]):
    def find_field_or_none(
        self, field_name: str, value: Union_primitive_types
    ) -> Optional[T]:
        pass


class CreateContract(Protocol, Generic[K]):
    def create(self, aggregate: K) -> None:
        pass
