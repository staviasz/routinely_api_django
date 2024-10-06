from abc import ABC, abstractmethod
from typing import Generic, Literal, Optional, TypeVar, TypedDict, Union

from main.adapters.uuidAdapter import UuidAdapter
from main.domain.value_objects.value_objects import ValueObject
from main.errors.domain import InvalidIdError
from main.errors.shared import CustomError, CustomErrorAbstract


class OBJ(TypedDict):
    pass


class Props(TypedDict, OBJ):
    id: str


T = TypeVar("T", bound=Props)


class ValueObjectType(TypedDict):
    value_object: ValueObject
    props: OBJ


class Entity(ABC, Generic[T]):
    __errors: list[CustomErrorAbstract] = []

    @property
    def id(self) -> str:
        return self.__id

    def _create_id(self, id: Optional[str], origin: Optional[str]) -> None:
        if id and not UuidAdapter.validate_uuid4(id):
            self._add_error(InvalidIdError(origin))

        self.__id = UuidAdapter.generate_uuid4() if not id else id

    def _errors(self) -> list[CustomErrorAbstract] | None:

        return self.__errors if len(self.__errors) > 0 else None

    def _add_error(
        self, error: CustomErrorAbstract | list[CustomErrorAbstract]
    ) -> None:
        if isinstance(error, list):
            for err in error:
                if not self.__exists_error_in_list_errors(err):
                    self.__errors.append(err)
            return

        if not self.__exists_error_in_list_errors(error):
            self.__errors.append(error)

    def _clear_errors(self) -> None:
        self.__errors.clear()

    def _validate_value_objects(
        self,
        entities: list[ValueObjectType],
    ) -> list[ValueObject]:

        results: list[ValueObject] = []
        for item in entities:
            valueObject = item["value_object"]
            props = item["props"]
            try:
                result = valueObject(props)
                results.append(result)
            except CustomError as e:
                self._add_error(e.errors)

        return results

    def _raize_errors(self) -> None:
        errors = self._errors()
        if errors:
            raise CustomError(errors)

    def __exists_error_in_list_errors(self, error: CustomErrorAbstract) -> bool:
        return any(x.message_error == error.message_error for x in self.__errors)

    @abstractmethod
    def _validate(self, props: T) -> None:
        pass
