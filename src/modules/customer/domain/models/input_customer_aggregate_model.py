from typing import Optional, TypedDict


class InputCustomerAggregateModel(TypedDict):
    id: Optional[str]
    name: str
    accepted_terms: bool
    email: str
    password: str
