from unittest.mock import patch
import pytest
from datetime import datetime
from typing import Any, Awaitable, Union

from main.contracts import EventContract, HandlerContract
from main.errors import CustomError
from main.infra import DispatcherEvents


def create_event(name: str) -> EventContract:
    class EventStub(EventContract):
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

    return EventStub(name)


def create_handler() -> HandlerContract:
    class HandlerStub(HandlerContract):
        def __init__(self) -> None:
            pass

        def handle(self, event: EventContract) -> Union[Awaitable[None], None]:
            pass

    return HandlerStub()


class TestDispatcherEvents:
    def setup_method(self) -> None:
        self.dispatcher = DispatcherEvents()

        self.event1 = create_event("event1")
        self.event2 = create_event("event2")

        self.handler1 = create_handler()
        self.handler2 = create_handler()
        self.handler3 = create_handler()

    def test_register(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)

        assert len(self.dispatcher.handlers()[self.event1.get_name()]) == 1
        assert self.dispatcher.handlers()[self.event1.get_name()] == [self.handler1]

        self.dispatcher.register(self.event1.get_name(), self.handler2)

        assert len(self.dispatcher.handlers()[self.event1.get_name()]) == 2
        assert self.dispatcher.handlers()[self.event1.get_name()] == [
            self.handler1,
            self.handler2,
        ]

    def test_error_if_handle_exists_in_event(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)
        with pytest.raises(CustomError) as e:
            self.dispatcher.register(self.event1.get_name(), self.handler1)

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 409,
            "messages_error": [
                f"Handler already registered for {self.event1.get_name()}.",
            ],
        }

    def test_has(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)

        assert self.dispatcher.has(self.event1.get_name(), self.handler1)
        assert not self.dispatcher.has(self.event1.get_name(), self.handler2)

    def test_clear_handlers(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)
        self.dispatcher.register(self.event1.get_name(), self.handler2)

        assert self.dispatcher.handlers() == {
            self.event1.get_name(): [self.handler1, self.handler2]
        }

        self.dispatcher.clear()

        assert self.dispatcher.handlers() == {}

    def test_remove_handler(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)
        self.dispatcher.register(self.event1.get_name(), self.handler2)

        assert self.dispatcher.handlers() == {
            self.event1.get_name(): [self.handler1, self.handler2]
        }

        self.dispatcher.remove(self.event1.get_name(), self.handler1)

        assert self.dispatcher.handlers() == {self.event1.get_name(): [self.handler2]}

        self.dispatcher.remove(self.event1.get_name(), self.handler1)

        assert self.dispatcher.handlers() == {self.event1.get_name(): [self.handler2]}

    def test_dispatch(self):
        self.dispatcher.register(self.event1.get_name(), self.handler1)
        self.dispatcher.register(self.event1.get_name(), self.handler2)
        self.dispatcher.register(self.event2.get_name(), self.handler3)

        with patch.object(self.handler1, "handle") as mock_perform, patch.object(
            self.handler2, "handle"
        ) as mock_perform2, patch.object(self.handler3, "handle") as mock_perform3:

            self.dispatcher.dispatch(self.event1)
            mock_perform.assert_called()
            mock_perform2.assert_called()
            mock_perform3.assert_not_called()
