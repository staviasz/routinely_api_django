from datetime import datetime, timedelta
from typing import Optional, TypedDict

from main.domain.entity import Entity
from modules.auth.domain.errors.require_user_id import RequireUserIdError


class SessionModel(TypedDict, total=False):
    id: Optional[str]
    user_id: str
    created_at: Optional[datetime]
    expires_at: Optional[datetime]


class SessionEntity(Entity[SessionModel]):
    def __init__(self, props: SessionModel) -> None:
        self._validate(props)
        super().__init__(props)

    def _validate(self, props: SessionModel) -> None:
        self._clear_errors()

        if not props.get("user_id"):
            self._add_error(RequireUserIdError())

        self._create_id()

        current_time = datetime.now()
        props["created_at"] = current_time
        props["expires_at"] = current_time + timedelta(days=7)

        self._raize_errors()
