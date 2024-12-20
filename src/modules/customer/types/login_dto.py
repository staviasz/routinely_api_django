from typing import TypedDict


class LoginInput(TypedDict):
    email: str
    password: str
    remember_me: bool


class LoginOutput(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
