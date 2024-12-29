from typing import (
    Generic,
    List,
    Literal,
    Optional,
    Protocol,
    TypeAlias,
    TypeVar,
    TypedDict,
    Union,
)

from main.domain.aggregates import Aggregate
from main.domain.entity import Entity

_T = TypeVar("_T", bound=Union[Entity, Aggregate], covariant=True)
_K = TypeVar("_K", bound=Union[Entity, Aggregate], contravariant=True)

Union_primitive_types = Union[str, int, float, bool, None]


class FindFieldOrNoneContract(Protocol, Generic[_T]):
    async def find_field_or_none(
        self, field_name: str, value: Union_primitive_types
    ) -> Optional[_T]:
        pass


class FindFieldContract(Protocol, Generic[_T]):
    async def find_field(self, field_name: str, value: Union_primitive_types) -> _T:
        pass


class DeleteContract(Protocol, Generic[_T]):
    async def delete(self, field_name: str, value: Union_primitive_types) -> None:
        pass


class CreateContract(Protocol, Generic[_K]):
    async def create(self, aggregate: _K) -> None:
        pass


class UpdateContract(Protocol, Generic[_K]):
    async def update(self, aggregate: _K) -> None:
        pass


order_types: TypeAlias = Literal["asc", "desc"]


class SearchParamsType(TypedDict, total=False):
    page: Optional[int]
    per_page: Optional[int]
    sort: Optional[str]
    order: Optional[order_types]


class SearchResultType(TypedDict, Generic[_T], total=False):
    items: list[_T]
    total: int
    current_page: int
    per_page: Optional[int]
    sort: Optional[str]
    order: Optional[order_types]


_E = TypeVar("_E", bound=Union[Entity, Aggregate])
_SearchParams = TypeVar("_SearchParams", contravariant=True)
_SearchResult = TypeVar("_SearchResult", covariant=True)


class SearchContract(
    Protocol,
    Generic[
        _E,
        _SearchParams,
        _SearchResult,
    ],
):
    async def search(self, props: _SearchParams) -> _SearchResult:
        pass

    async def _apply_sort(
        self, items: List[_E], sort: Optional[str], order: Optional[str]
    ) -> List[_E]:
        pass

    async def _apply_paginate(
        self, items: List[_E], page: Optional[int], per_page: Optional[int]
    ) -> List[_E]:
        pass
