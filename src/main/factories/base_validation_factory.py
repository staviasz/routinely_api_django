from typing import Type, TypeVar
from pydantic import BaseModel
from main import ValidatorContract, BaseValidationPydantic

T = TypeVar("T", bound=BaseModel)


def base_validation_factory(schema: Type[T]) -> ValidatorContract:
    return BaseValidationPydantic(schema=schema)
