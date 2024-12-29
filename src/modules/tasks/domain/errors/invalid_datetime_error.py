from typing import Optional
from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidDateTimeError(CustomErrorAbstract):
    def __init__(self, field: Optional[str] = None) -> None:
        date_formats = [
            "YYYY/mm/dd",
            "YYYY/mm/dd HH:MM",
            "YYYY/mm/dd HH:MM:SS",
            "YYYY/mm/ddTHH:MM:SS",
        ]
        super().__init__(
            code_error=400,
            message_error=f"The {field or "date_time"} is mandatory and must be in the formats {', '.join(date_formats)}",
        )
