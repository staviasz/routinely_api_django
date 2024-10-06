from main.errors.shared import CustomErrorAbstract


class InvalidAcceptedTermsError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error="The terms must be accepted.",
        )
