from abc import ABC
from typing import TypedDict, Union


class ObjectErrorType(TypedDict):
    code_error: int


class InputObjectErrorType(TypedDict, ObjectErrorType):
    message_error: str


class OutputObjectErrorType(TypedDict, ObjectErrorType):
    messages_error: list[str]


class CustomErrorAbstract(ABC):
    def __new__(cls, *args, **kwargs):
        if cls is CustomErrorAbstract:
            raise TypeError(
                f"{cls.__name__} is an abstract class and cannot be instantiated directly."
            )
        return super().__new__(cls)

    def __init__(self, code_error: int, message_error: str) -> None:
        self._code_error = code_error
        self._message_error = message_error

    @property
    def code_error(self) -> int:
        return self._code_error

    @property
    def message_error(self) -> str:
        return self._message_error


_Errors = Union[CustomErrorAbstract, list[CustomErrorAbstract]]


class CustomError(Exception):
    def __init__(self, errors: _Errors) -> None:
        self.__validate_construction(errors)
        self.__props = errors if isinstance(errors, list) else [errors]

    @property
    def errors(self) -> list[CustomErrorAbstract]:
        return self.__props

    @property
    def formate_errors(self) -> OutputObjectErrorType:
        return {
            "code_error": self.__props[0].code_error,
            "messages_error": [error.message_error for error in self.__props],
        }

    def __validate_construction(self, errors: _Errors) -> None:
        if isinstance(errors, CustomErrorAbstract):
            return

        if isinstance(errors, list) and all(
            isinstance(error, CustomErrorAbstract) for error in errors
        ):
            return

        raise TypeError(
            """O erro deve ser uma instância de CustomErrorAbstract ou uma
                lista de instâncias de CustomErrorAbstract."""
        )
