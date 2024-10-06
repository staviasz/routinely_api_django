from typing import Dict

import pytest

from main.domain.value_objects.value_objects import ValueObject
from main.errors.domain import InvalidIdError
from main.errors.shared import CustomErrorAbstract
from main.domain.entities.entity import Entity
from main.errors.shared import CustomError


class ErrorTest(CustomErrorAbstract):
    def __init__(self, message_error: str) -> None:
        super().__init__(code_error=400, message_error=message_error)


class ConcreteValueObject(ValueObject[str]):
    def __init__(self, props: str) -> None:
        self._validate(props)

    def _validate(self, props: str) -> None:
        self._clear_errors()
        if len(props) < 3:
            self._add_error(
                ErrorTest(
                    "The value object should have at least 3 characters.",
                )
            )

        self._raize_errors()


class ConcreteEntity(Entity[Dict[str, str]]):
    def __init__(self, props: Dict[str, str]) -> None:
        self._validate(props)

    def _validate(self, props: Dict[str, str]) -> None:
        self._clear_errors()

        self._create_id(props.get("id"), "ConcreteEntity")
        name = props.get("name")

        if name:
            self._validate_value_objects(
                [
                    {
                        "value_object": ConcreteValueObject,
                        "props": name,
                    }
                ]
            )

        self._raize_errors()


class TestEntity:

    def test_create_id_valid_uuid(self):
        id = "550e8400-e29b-41d4-a716-446655440000"
        props = {"id": id}
        entity = ConcreteEntity(props)
        assert entity.id == id

    def test_create_id_no_uuid(self):
        props = {"id": None}
        entity = ConcreteEntity(props)
        assert entity._errors() is None
        assert entity.id is not None

    def test_add_multiple_errors(self):
        props = {"id": None}
        entity = ConcreteEntity(props)
        error1 = ErrorTest("First error")
        error2 = ErrorTest("Second error")
        entity._add_error([error1, error2])
        assert len(entity._errors()) == 2
        assert entity._errors() == [error1, error2]

    def test_clear_errors(self):
        props = {"id": None}
        entity = ConcreteEntity(props)
        error = ErrorTest("First error")
        entity._add_error(error)
        entity._clear_errors()
        assert entity._errors() is None

    def test_raise_exception(self):
        props = {"id": "None", "name": "T"}
        with pytest.raises(CustomError) as e:
            ConcreteEntity(props)

        custom_error = e.value
        assert custom_error.formated_errors == {
            "code_error": 400,
            "messages_error": [
                "The id in ConcreteEntity is invalid.",
                "The value object should have at least 3 characters.",
            ],
        }

    def test_valid_entity(self):
        props = {"id": "550e8400-e29b-41d4-a716-446655440000", "name": "Test"}
        entity = ConcreteEntity(props)
        assert entity._errors() is None
