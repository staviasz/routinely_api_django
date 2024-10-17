from datetime import datetime
from typing import Any, Awaitable, List, Protocol, TypedDict, Union


class EventContract(Protocol):
    def get_name(self) -> str:
        pass

    def get_payload(self) -> dict[str, Any]:
        pass

    def set_payload(self, payload: dict[str, Any]) -> None:
        pass

    def get_datetime(self) -> datetime:
        pass


class HandlerContract(Protocol):
    def handle(self, event: EventContract) -> Union[Awaitable[None], None]:
        pass


class DispatcherContract(Protocol):
    def handlers(self) -> List[HandlerContract]:
        pass

    def register(self, name: str, handler: HandlerContract) -> None:
        pass

    def dispatch(self, event: EventContract) -> None:
        pass

    def remove(self, name: str, handler: HandlerContract) -> None:
        pass

    def has(self, name: str, handler: HandlerContract) -> bool:
        pass

    def clear(self) -> None:
        pass
