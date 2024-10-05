from main.errors.shared import CustomErrorAbstract


class InvalidNameError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error=f"The name must be between 3 and 70 characters and only letters",
        )
