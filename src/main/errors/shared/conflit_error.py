from main.errors import CustomErrorAbstract


class ConflitError(CustomErrorAbstract):
    def __init__(
        self, field_conflict: str | None = None, message_error: str | None = None
    ) -> None:
        message = message_error or f"Conflit: The {field_conflict} already exists."
        super().__init__(code_error=409, message_error=message)
