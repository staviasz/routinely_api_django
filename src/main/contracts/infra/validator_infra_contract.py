from typing import Protocol, Dict, Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel, covariant=True)


class ValidatorContract(Protocol[T]):
    def validate(self, props: Dict[str, Any]) -> T:
        pass

    def to_dict(self) -> T:
        pass
