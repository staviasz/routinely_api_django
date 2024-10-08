from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidFieldError(CustomErrorAbstract):
    def __init__(self, field: str) -> None:
        self.__validate_constructor(field)
        super().__init__(code_error=400, message_error=f"The {field} is invalid.")

    def __validate_constructor(self, field: str) -> None:
        if not field:
            raise ValueError(f"Invalid field: {field} in class InvalidFieldError")
