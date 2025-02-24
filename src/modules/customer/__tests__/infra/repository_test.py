import copy
import pytest
from modules.customer import repository_customer_factory, CustomerAggregate
from django_.models.models import CustomerDBModel, AccountDBModel
from asgiref.sync import sync_to_async

from modules.customer.domain.models.input_customer_aggregate_model import (
    InputCustomerAggregateModel,
)


repository = repository_customer_factory()
data: InputCustomerAggregateModel = {
    "name": "Test Customer",
    "accepted_terms": True,
    "email": "testCustomer@example.com",
    "password": "@Teste1",
}
aggregate = CustomerAggregate(data)


@pytest.mark.usefixtures("setup_database")
@pytest.mark.asyncio
class TestCustomerRepository:
    def setup_method(self):
        self.data = data
        self.aggregate = aggregate
        self.repository = repository

    async def test_create_customer(self):
        await self.repository.create(self.aggregate)

        customer = await sync_to_async(CustomerDBModel.objects.get)(
            id=self.aggregate.id
        )
        account = await sync_to_async(AccountDBModel.objects.get)(id=self.aggregate.id)
        expected_result = {
            "id": str(customer.id),
            "name": customer.name,
            "accepted_terms": customer.accepted_terms,
            "email": account.email,
            "is_active": account.is_active,
        }
        dict_aggregate = copy.deepcopy(self.aggregate.to_dict)
        del dict_aggregate["password"]
        assert expected_result == dict_aggregate

    async def test_find_field_customer_or_raise_error(self):
        with pytest.raises(Exception) as e:
            await self.repository.find_field(
                "id", "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0"
            )

        error = e.value
        assert error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Customer not found."],
        }

    async def test_find_field_by_customer(self):
        customer = await self.repository.find_field("name", self.aggregate.name)
        assert customer.to_dict == self.aggregate.to_dict

    async def test_find_field_by_account(self):
        customer = await self.repository.find_field("email", self.aggregate.email)
        assert customer.to_dict == self.aggregate.to_dict

    async def test_find_or_none_return_none(self):
        customer = await self.repository.find_field_or_none(
            "id", "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0"
        )
        assert customer is None

    async def test_find_or_none_return_customer(self):
        customer = await self.repository.find_field_or_none("id", self.aggregate.id)
        assert customer.to_dict == self.aggregate.to_dict

    async def test_update_customer_raise_error_if_customer_not_found(self):
        aggregate = CustomerAggregate(
            {
                "id": "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0",
                "name": "Test",
                "accepted_terms": True,
                "email": "test@example.com",
                "password": "@Teste1",
                "is_active": False,
            }
        )
        with pytest.raises(Exception) as e:
            await self.repository.update(aggregate)

        error = e.value
        assert error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Customer not found."],
        }

    async def test_update_customer(self):
        data = {
            **self.data,
            "id": self.aggregate.id,
            "name": "Test updated",
        }
        aggregate = CustomerAggregate(data)

        await self.repository.update(aggregate)
        customer = await sync_to_async(CustomerDBModel.objects.get)(
            id=self.aggregate.id
        )
        account = await sync_to_async(AccountDBModel.objects.get)(id=self.aggregate.id)
        expected_result = {
            "id": str(customer.id),
            "name": customer.name,
            "accepted_terms": customer.accepted_terms,
            "email": account.email,
            "is_active": account.is_active,
        }

        dict_aggregate = copy.deepcopy(aggregate.to_dict)
        del dict_aggregate["password"]
        assert expected_result == dict_aggregate

    async def test_delete_customer_raise_error_if_customer_not_found(self):
        with pytest.raises(Exception) as e:
            await self.repository.delete("id", "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0")

        error = e.value
        assert error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Customer not found."],
        }

    async def test_delete_customer(self):
        await self.repository.delete("id", self.aggregate.id)
        customer = await sync_to_async(
            lambda: CustomerDBModel.objects.filter(id=self.aggregate.id).first()
        )()

        assert customer is None
