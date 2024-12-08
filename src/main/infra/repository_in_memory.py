from typing import Generic, Optional, TypeVar, Union
from main.contracts import (
    FindFieldOrNoneContract,
    DeleteContract,
    FindFieldContract,
    Union_primitive_types,
    CreateContract,
)
from main.domain import Aggregate, Entity
from main.errors.shared.custom_error import CustomError, CustomErrorAbstract

T = TypeVar("T", bound=Union[Entity, Aggregate])


class RepositoryInMemoryException(CustomErrorAbstract):
    def __init__(self, code_error: int, message_error: str) -> None:
        super().__init__(code_error=code_error, message_error=message_error)


class RepositoryInMemory(
    FindFieldOrNoneContract[T],
    CreateContract[T],
    FindFieldContract[T],
    DeleteContract[T],
    Generic[T],
):
    def __init__(self) -> None:
        self.list_data: list[T] = []

    async def find_field_or_none(
        self, field_name: str, value: Union_primitive_types
    ) -> Optional[T]:
        for item in self.list_data:
            if getattr(item, field_name) == value:
                return item

        return None

    async def find_field(self, field_name: str, value: Union_primitive_types) -> T:
        for item in self.list_data:
            if getattr(item, field_name) == value:
                return item

        raise CustomError(
            RepositoryInMemoryException(
                code_error=404, message_error=f"{field_name} not found."
            )
        )

    async def create(self, aggregate: T) -> None:
        self.list_data.append(aggregate)

    async def delete(self, field_name: str, value: Union_primitive_types) -> None:
        for item in self.list_data:
            if getattr(item, field_name) == value:
                self.list_data.remove(item)
