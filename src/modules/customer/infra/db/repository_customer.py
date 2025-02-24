import asyncio
from typing import Optional, cast
from main import Union_primitive_types, CustomError, NotFoundError
from modules.customer import CustomerRepositoryContract, CustomerAggregate

from django_.models.customer_db_model import CustomerDBModel
from django_.models.account_db_model import AccountDBModel
from django.db import transaction
from asgiref.sync import sync_to_async

from modules.customer.infra.crypto.encryption import EncryptionAdapter


class RepositoryCustomer(CustomerRepositoryContract):
    def __init__(self, cripto: EncryptionAdapter) -> None:
        self.cripto = cripto

    async def find_field(
        self, field: str, value: Union_primitive_types
    ) -> CustomerAggregate:

        results = await self.find_by_customer_or_account(field, value)

        if not results:
            raise CustomError(NotFoundError("Customer not found."))

        customer, account = results

        return self.mapper_repository_to_domain(customer, account)

    async def find_field_or_none(
        self, field: str, value: Union_primitive_types
    ) -> Optional[CustomerAggregate]:
        results = await self.find_by_customer_or_account(field, value)

        if not results:
            return None

        customer, account = results

        return self.mapper_repository_to_domain(customer, account)

    async def create(self, aggregate: CustomerAggregate) -> None:
        await self.create_in_atomic(aggregate)
        return

    async def delete(self, field: str, value: Union_primitive_types) -> None:
        results = await self.find_by_customer_or_account(field, value)

        if not results:
            raise CustomError(NotFoundError("Customer not found."))

        (customer, _) = results

        await sync_to_async(customer.delete)()

        return None

    async def update(self, aggregate: CustomerAggregate) -> None:
        results = await self.find_by_customer_or_account("id", aggregate.id)

        if not results:
            raise CustomError(NotFoundError("Customer not found."))

        (customer, account) = results

        await self.update_in_atomic(customer, account, aggregate)

        return

    @sync_to_async
    def create_in_atomic(self, aggregate: CustomerAggregate):
        with transaction.atomic():
            customer = CustomerDBModel.objects.create(
                id=aggregate.id,
                name=aggregate.name,
                accepted_terms=aggregate.accepted_terms,
            )

            AccountDBModel.objects.create(
                id=aggregate.id,
                email=aggregate.email,
                password=self.encode(aggregate.password),
                is_active=aggregate.is_active,
                customer=customer,
            )

    @sync_to_async
    def update_in_atomic(
        self,
        customer: CustomerDBModel,
        account: AccountDBModel,
        aggregate: CustomerAggregate,
    ):
        with transaction.atomic():
            customer = CustomerDBModel.objects.get(id=aggregate.id)
            customer.name = aggregate.name
            customer.accepted_terms = aggregate.accepted_terms
            customer.save()

            account = AccountDBModel.objects.get(customer=customer)
            account.email = aggregate.email
            account.password = self.encode(aggregate.password)
            account.is_active = aggregate.is_active
            account.save()

    @sync_to_async
    def find_by_customer_or_account(
        self, field: str, value: Union_primitive_types
    ) -> Optional[tuple[CustomerDBModel, AccountDBModel]]:
        def customer_query(field, value) -> CustomerDBModel:
            return CustomerDBModel.objects.filter(**{field: value}).first()

        def account_query(field, value) -> AccountDBModel:
            return AccountDBModel.objects.filter(**{field: value}).first()

        first_query = (
            "customer" if field in ["id", "name", "accepted_terms"] else "account"
        )

        try:
            customer, account = None, None
            if first_query == "customer":
                customer = customer_query(field, value)
                if not customer:
                    return None
                account = account_query("id", customer.id)
            else:
                account = account_query(field, value)
                if not account:
                    return None
                customer = customer_query("id", account.id)

            return customer, account

        except Exception:
            raise CustomError(NotFoundError("Customer not found."))

    def encode(self, value: str) -> str:
        return self.cripto.encrypt(value)

    def decode(self, value: str) -> str:
        return self.cripto.decrypt(value)

    def mapper_repository_to_domain(
        self, customer: CustomerDBModel, account: AccountDBModel
    ) -> CustomerAggregate:
        return CustomerAggregate(
            {
                "id": str(customer.id),
                "name": customer.name,
                "accepted_terms": customer.accepted_terms,
                "email": account.email,
                "password": self.decode(account.password),
                "is_active": account.is_active,
            }
        )
