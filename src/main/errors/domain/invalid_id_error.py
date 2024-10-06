from main.errors.shared import CustomErrorAbstract


class InvalidIdError(CustomErrorAbstract):
    def __init__(self, original: str) -> None:
        self.__validate_constructor(original)
        super().__init__(
            code_error=400,
            message_error=f"The id in {original} is invalid.",
        )

    def __validate_constructor(self, original: str) -> None:
        if not original:
            raise ValueError("The original is required.")
