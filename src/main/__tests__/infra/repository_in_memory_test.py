from typing import Optional, TypedDict

import pytest
from main.domain import Entity
from main.errors.shared.custom_error import CustomError
from main.infra import RepositoryInMemory, RepositoryInMemorySearchable
from main.infra.repository.searchable import SearchParams


class EntityProps(TypedDict, total=False):
    id: Optional[str]
    name: str
    age: int


class EntityRepository(Entity[EntityProps]):
    def __init__(self, props: EntityProps) -> None:
        self.props = props
        self._create_id(self.props.get("id"), "Entity")
        super().__init__(props)

    @property
    def id(self) -> str:
        return self.__id

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


@pytest.mark.asyncio
class TestRepositoryInMemorySearchable:
    def setup_method(self):
        self.repository = RepositoryInMemorySearchable[EntityRepository]()

    async def test_apply_sort(self):
        arrange = [
            {"name": "brian", "age": 18},
            {"name": "Ane", "age": 20},
            {"name": "José", "age": 19},
            {"name": "Cristian", "age": 21},
        ]

        for item in arrange:
            entity = EntityRepository(item)
            await self.repository.create(entity)

        result = await self.repository._apply_sort(self.repository.list_data, "name")

        names = [item.name for item in result]

        assert names == ["Ane", "brian", "Cristian", "José"]

        result = await self.repository._apply_sort(
            self.repository.list_data, "name", "desc"
        )

        names = [item.name for item in result]

        assert names == ["José", "Cristian", "brian", "Ane"]

        result = await self.repository._apply_sort(self.repository.list_data, "age")

        ages = [item.age for item in result]

        assert ages == [18, 19, 20, 21]

        result = await self.repository._apply_sort(
            self.repository.list_data, "age", "desc"
        )

        ages = [item.age for item in result]

        assert ages == [21, 20, 19, 18]

    async def test_apply_paginate(self):
        arrange = [
            {"name": "brian", "age": 18},
            {"name": "Ane", "age": 20},
            {"name": "José", "age": 19},
        ]

        for item in arrange:
            entity = EntityRepository(item)
            await self.repository.create(entity)

        result = await self.repository._apply_paginate(self.repository.list_data, 1, 2)

        assert len(result) == 2

        result = await self.repository._apply_paginate(self.repository.list_data, 2, 2)

        assert len(result) == 1

        result = await self.repository._apply_paginate(self.repository.list_data, 3, 2)

        assert len(result) == 1

    async def test_apply_paginate_with_incorrect_params(self):
        arrange_data = [
            {"name": "brian", "age": 18},
            {"name": "Ane", "age": 20},
            {"name": "José", "age": 19},
        ]

        for item in arrange_data:
            entity = EntityRepository(item)
            await self.repository.create(entity)

        arrange = [
            {"page": 0, "per_page": 2},
            {"page": None, "per_page": 2},
            {"page": 1, "per_page": None},
            {"page": 1, "per_page": 0},
        ]

        for item in arrange:
            result = await self.repository._apply_paginate(
                self.repository.list_data, item["page"], item["per_page"]
            )

            assert len(result) == 3

    async def test_search(self):
        arrange = [
            {"name": "brian", "age": 18},
            {"name": "Ane", "age": 20},
            {"name": "José", "age": 19},
        ]

        for item in arrange:
            entity = EntityRepository(item)
            await self.repository.create(entity)

        result = await self.repository.search(SearchParams({"page": 1, "per_page": 2}))

        assert result.to_dict() == {
            "total": 3,
            "current_page": 1,
            "per_page": 2,
            "last_page": 2,
            "items": self.repository.list_data[0:2],
            "sort": None,
            "order": None,
        }
