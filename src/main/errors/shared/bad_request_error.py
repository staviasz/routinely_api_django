from main.errors import CustomErrorAbstract


class BadRequestError(CustomErrorAbstract):
    def __init__(self, message_error: str | None = None) -> None:
        message = message_error or "Bad request."
        super().__init__(code_error=400, message_error=message)
