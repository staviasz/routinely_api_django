from typing import Optional, TypedDict


class InputAccountEntityModel(TypedDict):
    id: Optional[str]
    email: str
    password: str
