from typing import TypeAlias, TypedDict


class NewPasswordInput(TypedDict):
    account_id: str
    password: str
    confirm_password: str


NewPasswordOutput: TypeAlias = None
