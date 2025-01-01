from typing import cast
from main import Union_primitive_types
from modules.customer import CustomerRepositoryContract, CustomerAggregate


class RepositoryCustomer(CustomerRepositoryContract):
    async def find_field(
        self, field: str, value: Union_primitive_types
    ) -> CustomerAggregate:
        return cast(CustomerAggregate, {})

    async def find_field_or_none(
        self, field: str, value: Union_primitive_types
    ) -> CustomerAggregate:
        return cast(CustomerAggregate, {})

    async def create(self, aggregate: CustomerAggregate) -> None:
        return

    async def delete(
        self, field: str, value: Union_primitive_types
    ) -> CustomerAggregate:
        return cast(CustomerAggregate, {})

    async def update(self, aggregate: CustomerAggregate) -> None:
        return
