from typing import cast
from main.contracts import DispatcherContract
from main.contracts import HandlerContract
from main.errors import CustomError, ConflitError


class DispatcherEvents(DispatcherContract):
    def __init__(self) -> None:
        self.__handlers_dict: dict[str, list[HandlerContract]] = {}

    def handlers(self):
        return self.__handlers_dict

    def register(self, name, handler):
        if self.has(name, handler):
            raise CustomError(
                ConflitError(message_error=f"Handler already registered for {name}.")
            )
        return self.__handlers_dict.setdefault(name, []).append(handler)

    def has(self, name, handler) -> bool:
        handlers_by_name = self.__handlers_dict.get(name)
        return handler in handlers_by_name if handlers_by_name else False

    def clear(self):
        self.__handlers_dict = {}

    def remove(self, name, handler):
        if self.has(name, handler):
            self.__handlers_dict[name].remove(handler)

    def dispatch(self, event):
        handlers_by_name = self.__handlers_dict.get(event.get_name())
        if handlers_by_name:
            for handler in handlers_by_name:
                handler.handle(event)
