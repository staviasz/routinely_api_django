import re
from main.domain.value_objects import ValueObject
from main.errors import FieldIsRequiredError, InvalidFieldError


class EmailValueObject(ValueObject[str]):
    def __init__(self, email: str) -> None:
        self._validate(email)
        super().__init__(email)

    def _validate(self, email: str) -> None:
        self._clear_errors()

        self.__has_email(email)
        self.__is_valid_email(email)

        self._raize_errors()

    def __has_email(self, email: str) -> None:
        if email is None or email.strip() == "":
            self._add_error(FieldIsRequiredError("email"))

    def __is_valid_email(self, email: str) -> None:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, email):
            self._add_error(InvalidFieldError("email"))
