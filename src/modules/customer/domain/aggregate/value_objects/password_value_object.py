import re
from main.domain import ValueObject
from main.errors import FieldIsRequiredError
from modules.customer.domain import InvalidPasswordError


class PasswordValueObject(ValueObject[str]):
    def __init__(self, password: str) -> None:
        self._validate(password)
        super().__init__(password)

    def _validate(self, password: str) -> None:
        self._clear_errors()

        self.__has_password(password)
        self.__is_valid_password(password)

        self._raize_errors()

    def __has_password(self, password: str) -> None:
        if not password:
            self._add_error(FieldIsRequiredError("password"))

    def __is_valid_password(self, password: str) -> None:
        password_regex = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*=])[a-zA-Z\d!@#$%&*=]{6,}$"
        )
        if not re.match(password_regex, password):
            self._add_error(InvalidPasswordError())
