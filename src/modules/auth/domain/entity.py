from datetime import datetime, timedelta
from typing import Optional, TypedDict

from main.domain.entity import Entity
from modules.auth.domain.errors.require_user_id import RequireUserIdError


class MaxExpiresAt(TypedDict):
    days: Optional[int]
    hours: Optional[int]
    seconds: Optional[int]
    milliseconds: Optional[int]
    minutes: Optional[int]


class SessionModel(TypedDict, total=False):
    id: Optional[str]
    user_id: str
    created_at: Optional[datetime]
    expires_at: Optional[datetime]
    max_expires_at: Optional[MaxExpiresAt]


class SessionEntity(Entity[SessionModel]):
    def __init__(self, props: SessionModel) -> None:
        self._validate(props)
        super().__init__(props)
        self.user_id = props["user_id"]
        self.created_at = props["created_at"]
        self.expires_at = props["expires_at"]

    def _validate(self, props: SessionModel) -> None:
        self._clear_errors()

        if not props.get("user_id"):
            self._add_error(RequireUserIdError())

        self._create_id()

        current_time = datetime.now()
        props["created_at"] = (
            current_time if not props.get("created_at") else props["created_at"]
        )
        props["expires_at"] = (
            current_time + timedelta(**props.get("max_expires_at") or {"days": 7})
            if not props.get("expires_at")
            else props["expires_at"]
        )

        self._raize_errors()
