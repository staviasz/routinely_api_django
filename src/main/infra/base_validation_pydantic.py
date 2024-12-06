from typing import Any, Dict, Type, TypeVar, cast

from pydantic import BaseModel

from main.contracts import ValidatorContract
from main.errors import CustomError, CustomErrorAbstract

T = TypeVar("T", bound=BaseModel)


class BaseValidationPydantic(ValidatorContract[T]):
    def __init__(self, schema: Type[T]) -> None:
        self._schema = schema

    def validate(self, props: Dict[str, Any]) -> T:
        try:
            self.__props = self._schema(**props)
            return self.__props
        except Exception as e:
            raise self.__format_error_to_messages(e)

    def to_dict(self) -> T:
        return cast(T, self.__props.__dict__)

    def __format_error_to_messages(self, error: Exception) -> CustomError:
        str_error = str(error).split("\n")
        ignore_values_in_error = ["validation error", "For further information visit"]
        formate_errors: list[CustomErrorAbstract] = []
        field_temp: str = ""

        for line in str_error:
            if any(x in line for x in ignore_values_in_error):
                continue

            if "[" not in line:
                field_temp = line
                continue

            formate_errors.append(
                self.__create_instance_error(
                    code_error=400,
                    message_error=self.__fomat_message_error(
                        field_temp, self.__validate_sting_error(line)
                    ),
                )
            )
        return CustomError(formate_errors)

    def __create_instance_error(
        self, code_error: int, message_error: str
    ) -> CustomErrorAbstract:
        class Error(CustomErrorAbstract):
            pass

        return Error(code_error=code_error, message_error=message_error)

    def __fomat_message_error(self, field: str | None, message_error: str) -> str:
        if field is None or field == "":
            return message_error
        return f"{field}: {message_error}"

    def __validate_sting_error(self, error_str: str) -> str:
        error_str = error_str.split("[")[0].strip()
        error_str = (
            error_str.split("Value error, ")[1].strip()
            if "Value error, " in error_str
            else error_str
        )

        return error_str
