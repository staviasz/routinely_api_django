from typing import TypedDict

import pytest
from main.domain import Entity
from main.errors.shared.custom_error import CustomError
from main.infra import RepositoryInMemory


class EntityProps(TypedDict):
    id: str
    name: str
    age: int


class EntityRepository(Entity[EntityProps]):
    def __init__(self, props: EntityProps) -> None:
        self.props = props

    @property
    def id(self) -> str:
        return self.props["id"]

    @property
    def name(self) -> str:
        return self.props["name"]

    @property
    def age(self) -> int:
        return self.props["age"]

    def _validate(self, props: EntityProps) -> None:
        pass


@pytest.mark.asyncio
class TestRepositoryInMemory:

    def setup_method(self, method):
        self.repository = RepositoryInMemory[EntityRepository]()

    async def test_find_field_or_none_return_none(self):
        item = await self.repository.find_field_or_none("name", "Test")

        assert item is None

    async def test_find_field_or_none_return_item(self):
        data = {"id": "1", "name": "John", "age": 18}
        self.repository.list_data.append(EntityRepository(data))
        item = await self.repository.find_field_or_none("name", "John")

        assert item.props == data

    async def test_create(self):
        data = {"id": "1", "name": "John", "age": 18}
        await self.repository.create(EntityRepository(data))

        assert self.repository.list_data[0].props == data

    async def test_find_field_exception(self):
        field_name = "name"
        value = "John"
        with pytest.raises(CustomError) as e:
            await self.repository.find_field(field_name, value)

        print(e.value.formate_errors)
        assert e.value.formate_errors == {
            "code_error": 404,
            "messages_error": [f"{field_name} not found."],
        }

    async def test_find_field(self):
        data = {"id": "1", "name": "John", "age": 18}
        self.repository.list_data.append(EntityRepository(data))
        item = await self.repository.find_field("name", "John")

        assert item.props == data

    async def test_delete(self):
        data = {"id": "1", "name": "John", "age": 18}
        self.repository.list_data.append(EntityRepository(data))
        await self.repository.delete("name", "John")

        assert len(self.repository.list_data) == 0
