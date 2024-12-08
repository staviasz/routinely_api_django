from typing import Optional, TypedDict


class SessionInput(TypedDict):
    id: str


class SessionOutput(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
