from typing import Generic, Optional, TypeVar, Union
from main.contracts import (
    FindFieldOrNoneContract,
    Union_primitive_types,
    CreateContract,
)
from main.domain import Aggregate, Entity

T = TypeVar("T", bound=Union[Entity, Aggregate])


class RepositoryInMemory(FindFieldOrNoneContract[T], CreateContract[T], Generic[T]):
    def __init__(self) -> None:
        self.list_data: list[T] = []

    def find_field_or_none(
        self, field_name: str, value: Union_primitive_types
    ) -> Optional[T]:
        for item in self.list_data:
            print(type(item))
            if getattr(item, field_name) == value:
                return item

        return None

    def create(self, aggregate: T) -> None:
        self.list_data.append(aggregate)
