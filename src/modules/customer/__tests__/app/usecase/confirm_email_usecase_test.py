import pytest
from main import RepositoryInMemory
from modules.customer import CustomerAggregate, ConfirmEmailUsecase


class ConfirmEmailRepositoryInMemory(RepositoryInMemory[CustomerAggregate]):
    pass


@pytest.mark.asyncio
class TestConfirmEmailUsecase:
    def setup_method(self):
        self.repository = ConfirmEmailRepositoryInMemory()
        self.usecase = ConfirmEmailUsecase(self.repository)
        self.data = {
            "email": "G0s7B@example.com",
            "password": "@Teste123",
            "accepted_terms": True,
            "name": "Teste",
        }
        self.customer = CustomerAggregate(self.data)

    async def test_perform(self):
        self.repository.list_data.append(self.customer)

        await self.usecase.perform(self.data)

        customer = self.repository.list_data[0]
        assert customer.is_active
