from typing import Optional, TypedDict


class SessionTokens(TypedDict):
    access_token: str
    refresh_token: str


class SessionInput(TypedDict, total=False):
    user_id: Optional[str]
    tokens: Optional[SessionTokens]


class SessionOutput(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
