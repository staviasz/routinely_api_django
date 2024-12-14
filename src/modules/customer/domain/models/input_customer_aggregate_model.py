from typing import Optional, TypedDict


class InputCustomerAggregateModel(TypedDict, total=False):
    id: Optional[str]
    name: str
    accepted_terms: bool
    email: str
    password: str
    is_active: Optional[bool]
