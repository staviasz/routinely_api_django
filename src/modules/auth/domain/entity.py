from typing import Optional, TypedDict

from main.domain.entity import Entity


class SessionModel(TypedDict):
    id: Optional[str]
    token: str


class SessionEntity(Entity[SessionModel]):
    def __init__(self, props: SessionModel) -> None:
        self._validate(props)
        super().__init__(props)

    def _validate(self, props: SessionModel) -> None:
        self._clear_errors()
        self._create_id(props.get("id"), "SessionEntity")
        self._raize_errors()
