import re
from main.domain.value_objects.value_objects import ValueObject
from main.errors.domain import FieldIsRequiredError
from modules.customer.domain.errors import InvalidNameError


class NameValueObject(ValueObject[str]):
    def __init__(self, name: str) -> None:
        self._validate(name)
        super().__init__(name)

    def _validate(self, props: str) -> None:
        self._clear_errors()

        name = props.strip()

        if not self.__has_name(name):
            self._add_error(FieldIsRequiredError("name"))

        if not self.__is_valid_name(name) or not self.__name_length_is_valid(name):
            self._add_error(InvalidNameError())

        self._raize_errors()

    def __has_name(self, name: str) -> bool:
        return name is not None and name != ""

    def __is_valid_name(self, name: str) -> bool:
        regex = r"^[a-zA-ZÀ-ÿ\s~]+$"
        return bool(re.match(regex, name))

    def __name_length_is_valid(self, name: str) -> bool:
        return name is not None and len(name) >= 3 and len(name) < 70
