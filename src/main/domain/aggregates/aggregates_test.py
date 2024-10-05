from typing import Any, cast
import pytest
from unittest.mock import MagicMock
from main.domain.aggregates.aggregates import Aggregate, Props
from main.domain.entities.entity import Entity
from main.errors.domain import InvalidIdError
from main.errors.shared import CustomErrorAbstract
from main.adapters.uuidAdapter import UuidAdapter
from main.errors.shared import CustomError


class Error(CustomErrorAbstract):
    def __init__(self, message_error: str) -> None:
        self._message_error = message_error
        super().__init__(400, message_error)


class Entity1(Entity[dict[str, Any]]):
    def __init__(self, props: dict[str, Any]) -> None:
        self._validate(props)

    @property
    def name(self) -> str:
        return str(self._name)

    def _validate(self, props: dict[str, Any]) -> None:
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


class Entity2(Entity[dict[str, Any]]):
    def __init__(self, props: dict[str, Any]) -> None:
        self._validate(props)

    @property
    def age(self) -> int | None:
        return int(self._age) if self._age else None

    def _validate(self, props: dict[str, Any]) -> None:
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


class ConcreteAggregate(Aggregate[dict[str, Any]]):

    def __init__(self, props: dict[str, Any]) -> None:
        self._validate(props)

    def _validate(self, props: dict[str, Any]) -> None:
        self._clear_errors()
        self._create_id(props.get("id"), "ConcreteAggregate")

        entity1 = {"id": props.get("id"), "name": props.get("name")}
        entity2 = {"id": props.get("id"), "age": props.get("age")}

        entities = self._validate_entities(
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

        class_entity1 = cast(Entity1, entities[0])
        class_entity2 = cast(Entity2, entities[1])

        self.to_dict = {
            "id": self.id,
            "entity1": {"id": class_entity1.id, "name": class_entity1.name},
            "entity2": {"id": class_entity2.id, "age": class_entity2.age},
        }


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
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in ConcreteAggregate is invalid.",
                "The id in Entity1 is invalid.",
                "Name should have at least 3 characters.",
                "The id in Entity2 is invalid.",
            ],
        }
