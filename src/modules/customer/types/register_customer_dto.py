from typing import TypedDict, TypeAlias

from modules.customer import InputCustomerAggregateModel


class RegisterCustomerInput(TypedDict, InputCustomerAggregateModel):
    callback_url: str


RegisterCustomerOutput: TypeAlias = None
