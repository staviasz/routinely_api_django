from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidNameTaskError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error="The name is mandatory and must be up to 50 characters long",
        )
