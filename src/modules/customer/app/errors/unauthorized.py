from main.errors.shared.custom_error import CustomErrorAbstract


class UnauthorizedError(CustomErrorAbstract):
    def __init__(self, message_error: str = "Invalid credentials") -> None:
        super().__init__(code_error=401, message_error=message_error)
