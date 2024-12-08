from main.errors.shared.custom_error import CustomErrorAbstract


class RequireUserIdError(CustomErrorAbstract):
    def __init__(self):
        super().__init__(
            code_error=400,
            message_error="The user id is required.",
        )
