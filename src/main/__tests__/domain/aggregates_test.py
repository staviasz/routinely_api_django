from typing import Any, TypedDict, cast
import pytest
from main.domain import Entity, Aggregate
from main.errors import CustomErrorAbstract, CustomError


class Error(CustomErrorAbstract):
    def __init__(self, message_error: str) -> None:
        self._message_error = message_error
        super().__init__(400, message_error)


class Entity1Props(TypedDict):
    id: str
    name: str


class Entity1(Entity[Entity1Props]):
    def __init__(self, props: Entity1Props) -> None:
        self._validate(props)

    @property
    def name(self) -> str:
        return str(self._name)

    def _validate(self, props: Entity1Props) -> None:
        self._clear_errors()
        self._create_id(props.get("id"), "Entity1")

        if props.get("name") and len(props["name"]) < 3:
            self._add_error(
                Error(
                    "Name should have at least 3 characters.",
                )
            )

        self._raize_errors()

        self._name = props.get("name")


class Entity2Props(TypedDict):
    id: str
    age: int


class Entity2(Entity[Entity2Props]):
    def __init__(self, props: Entity2Props) -> None:
        self._validate(props)

    @property
    def age(self) -> int | None:
        return int(self._age) if self._age else None

    def _validate(self, props: Entity2Props) -> None:
        self._clear_errors()
        self._create_id(props.get("id"), "Entity2")

        if props.get("age") and int(props["age"]) < 18:
            self._add_error(
                Error(
                    "Age should be at least 18.",
                )
            )

        self._raize_errors()

        self._age = props.get("age")


class AggregateProps(TypedDict):
    id: str
    name: str
    age: int


class ConcreteAggregate(Aggregate[AggregateProps]):

    def __init__(self, props: AggregateProps) -> None:
        self._validate(props)
        self.__props = props

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "entity1": {"id": self.id, "name": self.__props.get("name")},
            "entity2": {"id": self.id, "age": self.__props.get("age")},
        }

    def _validate(self, props: AggregateProps) -> None:
        self._clear_errors()
        self._create_id(props.get("id"), "ConcreteAggregate")

        entity1 = {"id": props.get("id"), "name": props.get("name")}
        entity2 = {"id": props.get("id"), "age": props.get("age")}

        self._validate_entities(
            [
                {
                    "entity": Entity1,
                    "props": entity1,
                },
                {
                    "entity": Entity2,
                    "props": entity2,
                },
            ]
        )

        self._raize_errors()


class TestAggregate:
    def test_create_id_valid_uuid(self):
        id = "550e8400-e29b-41d4-a716-446655440000"
        props = {"id": id, "name": "John", "age": 18}
        aggregate = ConcreteAggregate(props)
        assert aggregate._errors() is None
        assert aggregate.id == id
        assert aggregate.to_dict == {
            "id": id,
            "entity1": {"id": id, "name": "John"},
            "entity2": {"id": id, "age": 18},
        }

    def test_create_id_no_uuid(self):
        props = {"id": None, "entity1": "John", "entity2": 18}
        aggregate = ConcreteAggregate(props)
        assert aggregate._errors() is None
        assert aggregate.id is not None

    def test_raise_error(self):
        props = {"id": "None", "name": "Jo", "age": 18}

        with pytest.raises(CustomError) as e:
            ConcreteAggregate(props)

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in ConcreteAggregate is invalid.",
                "The id in Entity1 is invalid.",
                "Name should have at least 3 characters.",
                "The id in Entity2 is invalid.",
            ],
        }
