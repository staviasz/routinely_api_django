from typing import TypedDict


class ConfirmCodeToResetPasswordInput(TypedDict):
    code: str
    id: str
