from typing import TypedDict


class ForgetPasswordInput(TypedDict):
    email: str


class ForgetPasswordOutput(TypedDict):
    account_id: str
