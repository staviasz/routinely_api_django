import re
from main.domain import ValueObject
from main.errors import FieldIsRequiredError
from modules.customer.domain import InvalidNameError


class NameValueObject(ValueObject[str]):
    def __init__(self, name: str) -> None:
        self._validate(name)
        super().__init__(name)

    def _validate(self, props: str) -> None:
        self._clear_errors()

        self.__has_name(props)

        name = props.strip()
        self.__is_valid_name(name)
        self.__name_length_is_valid(name)

        self._raize_errors()

    def __has_name(self, name: str) -> None:
        if name is None or name.strip() == "":
            self._add_error(FieldIsRequiredError("name"))
        return

    def __is_valid_name(self, name: str) -> None:
        regex = r"^[a-zA-ZÀ-ÿ\s~]+$"
        if not re.match(regex, name):
            self._add_error(InvalidNameError())
        return

    def __name_length_is_valid(self, name: str) -> None:
        if len(name) < 3 or len(name) > 70:
            self._add_error(InvalidNameError())
        return
