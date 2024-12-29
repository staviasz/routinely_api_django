from math import ceil
from typing import Optional, TypeVar, Union, cast, Generic
from main.contracts.infra.repository_infra_contract import (
    SearchParamsType,
    SearchResultType,
    order_types,
)
from main.domain.aggregates import Aggregate
from main.domain.entity import Entity

T = TypeVar("T", bound=Union[Entity, Aggregate])


class SearchParams:
    page: int = 1
    per_page: Optional[int] = None
    sort: Optional[str] = None
    order: Optional[order_types] = None

    def __init__(self, props: SearchParamsType = {}) -> None:
        self.page = self.__page(props.get("page") or 1)
        self.per_page = self.__per_page(props.get("per_page"))
        self.sort = self.__sort(props.get("sort"))
        self.order = self.__order(props.get("order"))

    def __page(self, value: int) -> int:
        if not isinstance(value, int):
            try:
                value = int(float(value))
            except Exception:
                value = 1

        return value if value > 0 else self.page

    def __per_page(self, value: Optional[int]) -> Optional[int]:
        if not isinstance(value, int) and value is not None:
            try:
                value = int(float(value))
            except Exception:
                value = None

        if isinstance(value, bool):
            value = None

        return value if value and value > 0 else None

    def __sort(self, value: Optional[str]) -> Optional[str]:
        if value and isinstance(value, str) and value.strip() != "":
            return value
        return None

    def __order(self, value: Optional[str]) -> Optional[order_types]:
        if not value or not isinstance(value, str):
            return None

        normalized_value = cast(order_types, value.lower())
        return normalized_value if normalized_value in ["asc", "desc"] else "asc"


class SearchResult(Generic[T]):
    def __init__(self, props: SearchResultType) -> None:
        self.items = props.get("items", [])
        self.total = props.get("total", 0)
        self.current_page = props.get("current_page", 1)
        self.per_page = props.get("per_page", None)
        self.last_page = ceil(self.total / self.per_page) if self.per_page else 1
        self.sort = props.get("sort", None)
        self.order = props.get("order", None)

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "current_page": self.current_page,
            "per_page": self.per_page,
            "last_page": self.last_page,
            "sort": self.sort,
            "order": self.order,
        }
