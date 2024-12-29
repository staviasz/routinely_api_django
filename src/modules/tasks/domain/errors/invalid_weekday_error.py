from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidWeekdayError(CustomErrorAbstract):
    def __init__(self) -> None:
        super().__init__(
            code_error=400,
            message_error="The Weekdays must be a valid day of the week",
        )
