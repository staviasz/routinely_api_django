from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar, Union
from main.errors import CustomErrorAbstract, CustomError


_Props = Union[Dict[str, Any], str, bool]


T = TypeVar("T", bound=_Props)


class ValueObject(ABC, Generic[T]):
    __errors: list[CustomErrorAbstract] = []

    def __init__(self, props: T) -> None:
        self.__props = props

    @property
    def value(self) -> T:
        return self.__props

    def _errors(self) -> list[CustomErrorAbstract] | None:
        return self.__errors if len(self.__errors) > 0 else None

    def _add_error(self, error: CustomErrorAbstract) -> None:
        if not any(x.message_error == error.message_error for x in self.__errors):
            self.__errors.append(error)

    def _clear_errors(self) -> None:
        self.__errors.clear()

    def _raize_errors(self) -> None:
        errors = self._errors()
        print("errors", errors)
        if errors:
            raise CustomError(errors)

    @abstractmethod
    def _validate(self, props: T) -> None:
        pass
