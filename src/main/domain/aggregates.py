from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    Generic,
    Literal,
    Optional,
    Type,
    TypeVar,
    TypedDict,
    Union,
    cast,
)

from main.adapters import UuidAdapter
from main.domain.entity import Entity
from main.errors import InvalidIdError, CustomError, CustomErrorAbstract


class OBJ(TypedDict):
    pass


class EntityType(TypedDict):
    entity: Type[Entity]
    props: Dict[str, Any]


T = TypeVar("T", bound=OBJ)


class Aggregate(ABC, Generic[T]):
    _error_list: list[CustomErrorAbstract] = []

    def __init__(self, props: T) -> None:
        self.__props = props

    @property
    def id(self) -> str:
        return self.__id

    @property
    def to_dict(self) -> T:
        return self.__props

    def _create_id(self, id: Optional[str], origin: Optional[str]) -> None:
        if id and not UuidAdapter.validate_uuid4(id):
            self._add_error(InvalidIdError(original=cast(str, origin)))

        self.__id = UuidAdapter.generate_uuid4() if not id else id

    def _errors(self) -> list[CustomErrorAbstract] | None:

        return self._error_list if len(self._error_list) > 0 else None

    def _add_error(
        self, error: CustomErrorAbstract | list[CustomErrorAbstract]
    ) -> None:
        if isinstance(error, list):
            for err in error:
                if not self.__exists_error_in_list_errors(err):
                    self._error_list.append(err)
            return

        if not self.__exists_error_in_list_errors(error):
            self._error_list.append(error)

    def _clear_errors(self) -> None:
        self._error_list.clear()

    def _validate_entities(self, entities: list[EntityType]) -> list[Entity]:
        results: list[Entity] = []
        for item in entities:
            entity: Type[Entity] = item["entity"]
            props = item["props"]
            try:
                result = entity(props)
                results.append(result)
            except CustomError as e:
                self._add_error(e.errors)

        return results

    def _raize_errors(self) -> None:
        errors = self._errors()
        if errors:
            raise CustomError(errors)

    def __exists_error_in_list_errors(self, error: CustomErrorAbstract) -> bool:
        return any(x.message_error == error.message_error for x in self._error_list)

    @abstractmethod
    def _validate(self, props: T) -> None:
        pass
