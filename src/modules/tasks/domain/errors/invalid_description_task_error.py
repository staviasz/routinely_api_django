from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidDescriptionTaskError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error="The Description is mandatory and must be up to 1000 characters long",
        )
