from typing import TypedDict
from main.domain import Entity
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


class TestRepositoryInMemory:
    def test_find_fild_or_none_return_none(self):
        repository = RepositoryInMemory[EntityRepository]()
        item = repository.find_field_or_none("name", "Test")

        assert item is None

    def test_find_fild_or_none_return_item(self):
        data = {"id": "1", "name": "John", "age": 18}
        repository = RepositoryInMemory[EntityRepository]()
        repository.list_data.append(EntityRepository(data))
        item = repository.find_field_or_none("name", "John")

        assert item.props == data

    def test_create(self):
        repository = RepositoryInMemory[EntityRepository]()
        data = {"id": "1", "name": "John", "age": 18}
        repository.create(EntityRepository(data))

        assert repository.list_data[0].props == data
