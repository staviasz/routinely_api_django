from abc import ABC, abstractmethod
from typing import Generic, Literal, Optional, TypeVar, TypedDict, Union, Any

from main.adapters.uuidAdapter import UuidAdapter
from main.domain.entities.entity import Entity
from main.errors.domain import InvalidIdError
from main.errors.shared import CustomError, CustomErrorAbstract


class OBJ(TypedDict):
    pass


class Props(TypedDict, OBJ):
    id: str


class EntityType(TypedDict):
    entity: Entity
    props: OBJ


T = TypeVar("T", bound=Props)


class Aggregate(ABC, Generic[T]):
    _error_list: list[CustomErrorAbstract] = []
    _props: T

    @property
    def id(self) -> str:
        return self.__id

    @property
    def to_dict(self) -> T:
        return self._props

    @to_dict.setter
    def to_dict(self, props: T) -> None:
        self._props = props

    def _create_id(self, id: Optional[str], origin: Optional[str]) -> None:
        if id and not UuidAdapter.validate_uuid4(id):
            self._add_error(InvalidIdError(origin))

        self.__id = UuidAdapter.generate_uuid4() if not id else id

    def _errors(self) -> list[CustomErrorAbstract] | None:

        return self._error_list if len(self._error_list) > 0 else None

    def _add_error(
        self, error: CustomErrorAbstract | list[CustomErrorAbstract]
    ) -> None:
        if isinstance(error, list):
            self._error_list.extend(error)
            return

        self._error_list.append(error)

    def _clear_errors(self) -> None:
        self._error_list.clear()

    def _validate_entities(self, entities: list[EntityType]) -> list[Entity]:
        results: list[Entity] = []
        for item in entities:
            entity = item["entity"]
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

    @abstractmethod
    def _validate(self, props: T) -> None:
        pass
