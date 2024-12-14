from typing import TypedDict


class ConfirmCodeToResetPasswordInput(TypedDict):
    code: str
    email: str
