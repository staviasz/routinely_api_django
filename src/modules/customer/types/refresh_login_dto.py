from typing import TypedDict


class RefreshLoginInput(TypedDict):
    access_token: str
    refresh_token: str


class RefreshLoginOutput(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
