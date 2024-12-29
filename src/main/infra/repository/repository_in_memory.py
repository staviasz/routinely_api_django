from math import ceil
from typing import Generic, List, Optional, TypeVar, Union
import unicodedata
from main.contracts import (
    FindFieldOrNoneContract,
    DeleteContract,
    FindFieldContract,
    Union_primitive_types,
    CreateContract,
    UpdateContract,
    SearchContract,
)
from main.domain import Aggregate, Entity
from main.errors.shared.custom_error import CustomError, CustomErrorAbstract
from main.infra.repository.searchable import SearchParams, SearchResult

T = TypeVar("T", bound=Union[Entity, Aggregate])


class RepositoryInMemoryException(CustomErrorAbstract):
    def __init__(self, code_error: int, message_error: str) -> None:
        super().__init__(code_error=code_error, message_error=message_error)


class RepositoryInMemory(
    FindFieldOrNoneContract[T],
    CreateContract[T],
    FindFieldContract[T],
    UpdateContract[T],
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

    async def update(self, aggregate: T) -> None:
        for item in self.list_data:
            if item.id == aggregate.id:
                self.list_data.remove(item)
                self.list_data.append(aggregate)


class RepositoryInMemorySearchable(
    RepositoryInMemory[T], SearchContract[T, SearchParams, SearchResult[T]], Generic[T]
):

    async def search(self, props: SearchParams) -> SearchResult[T]:
        items_sorted = await self._apply_sort(self.list_data, props.sort, props.order)
        items_paginate = await self._apply_paginate(
            items_sorted, props.page, props.per_page
        )
        return SearchResult(
            {
                "items": items_paginate,
                "total": len(items_sorted),
                "current_page": props.page,
                "per_page": props.per_page,
                "order": props.order,
                "sort": props.sort,
            }
        )

    async def _apply_sort(
        self, items: List[T], sort: Optional[str], order: Optional[str] = "asc"
    ) -> List[T]:
        if sort and hasattr(items[0], sort):
            reverse = True if order == "desc" else False
            str_instance = isinstance(getattr(items[0], sort), str)

            if str_instance:
                return sorted(
                    items,
                    key=lambda x: self.__normalize_string(getattr(x, sort)),
                    reverse=reverse,
                )

            return sorted(items, key=lambda x: getattr(x, sort), reverse=reverse)
        return items

    async def _apply_paginate(
        self, items: List[T], page: Optional[int], per_page: Optional[int]
    ) -> List[T]:
        if per_page is None or page is None or page < 1 or per_page < 1:
            return items

        last_page = ceil(len(items) / per_page)
        page = page if page <= last_page else last_page

        start = (page - 1) * per_page
        end = start + per_page
        return items[start:end]

    def __normalize_string(self, s: str) -> str:
        return (
            unicodedata.normalize("NFD", s)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )
