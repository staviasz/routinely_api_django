from abc import ABC
from datetime import datetime
from typing import Any, Awaitable, List, Protocol, Union


class EventBaseClass(ABC):
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__payload: dict[str, Any] = {}
        self.__datetime: datetime

    def get_name(self) -> str:
        return self.__name

    def get_payload(self) -> dict[str, Any]:
        return self.__payload

    def set_payload(self, payload: dict[str, Any]) -> None:
        self.__payload = payload
        self.__datetime = datetime.now()

    def get_datetime(self) -> datetime:
        return self.__datetime


class HandlerContract(Protocol):
    def handle(self, event: EventBaseClass) -> None:
        pass


class DispatcherContract(Protocol):
    def handlers(self) -> List[HandlerContract]:
        pass

    def register(self, name: str, handler: HandlerContract) -> None:
        pass

    def dispatch(self, event: EventBaseClass) -> None:
        pass

    def remove(self, name: str, handler: HandlerContract) -> None:
        pass

    def has(self, name: str, handler: HandlerContract) -> bool:
        pass

    def clear(self) -> None:
        pass
