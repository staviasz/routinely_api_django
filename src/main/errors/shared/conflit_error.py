from main.errors import CustomErrorAbstract


class ConflitError(CustomErrorAbstract):
    def __init__(self, field_conflict: str) -> None:
        super().__init__(
            code_error=409,
            message_error=f"Conflit: The {field_conflict} already exists.",
        )
