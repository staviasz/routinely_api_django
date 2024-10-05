from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar, Union
from main.errors.shared import CustomErrorAbstract, CustomError


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
        if not isinstance(error, CustomErrorAbstract):
            raise TypeError(
                "O erro deve ser uma instância de CustomErrorAbstract.",
            )

        self.__errors.append(error)

    def _clear_errors(self) -> None:
        self.__errors.clear()

    def _raize_errors(self) -> None:
        errors = self._errors()
        if errors:
            raise CustomError(errors)

    @abstractmethod
    def _validate(self, props: T) -> None:
        pass
