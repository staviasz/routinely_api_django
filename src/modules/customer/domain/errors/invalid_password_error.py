from main.errors import CustomErrorAbstract


class InvalidPasswordError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error="The password must contain at least one uppercase letter, one lowercase letter, one special character, one number and be at least 6 characters long",
        )
