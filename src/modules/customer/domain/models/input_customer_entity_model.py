from typing import Optional, TypedDict


class InputCustomerEntityModel(TypedDict):
    id: Optional[str]
    name: str
    accepted_terms: bool
