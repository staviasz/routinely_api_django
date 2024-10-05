from main.errors.shared import CustomErrorAbstract


class FieldIsRequired(CustomErrorAbstract):
    def __init__(self, field: str) -> None:
        self.__validate_constructor(field)
        super().init_props(code_error=400, message_error=f"The {field} is required.")

    def __validate_constructor(self, field: str) -> None:
        if not field:
            raise ValueError(f"The {field} is required. in class FieldIsRequired")
