from main.errors import CustomErrorAbstract


class NotFoundError(CustomErrorAbstract):
    def __init__(self, message_error: str | None = None) -> None:
        message = message_error or "Not found."
        super().__init__(code_error=409, message_error=message)
