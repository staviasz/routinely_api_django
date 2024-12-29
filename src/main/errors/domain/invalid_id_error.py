from typing import Optional
from main.errors.shared.custom_error import CustomErrorAbstract


class InvalidIdError(CustomErrorAbstract):
    def __init__(
        self, custom_field: Optional[str] = None, original: Optional[str] = None
    ) -> None:
        super().__init__(
            code_error=400,
            message_error=f"The {custom_field or "id"} {f"in {original}" if original else ""} is invalid.",
        )
