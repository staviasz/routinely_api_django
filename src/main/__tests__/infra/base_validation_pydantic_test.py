from pydantic import BaseModel, Field
import pytest

from main.errors import CustomError
from main.infra import BaseValidationPydantic


class Schema(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(ge=18)
    cnh: bool


schema = BaseValidationPydantic(Schema)


class TestSchemaBase:
    def test_validate(self):
        props = {"name": "John", "age": 30, "cnh": True}
        result = schema.validate(props)
        assert result.__dict__ == props

    def test_unique_error_one_field(self):
        props = {"name": "J", "age": 30, "cnh": True}

        with pytest.raises(Exception) as e:
            schema.validate(props)

        assert isinstance(e.value, CustomError)
        assert e.value.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "name: String should have at least 3 characters",
            ],
        }

    def test_many_errors_one_field(self):
        props = {"name": "J", "age": "17", "cnh": True}

        with pytest.raises(Exception) as e:
            schema.validate(props)

        assert isinstance(e.value, CustomError)
        assert e.value.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "name: String should have at least 3 characters",
                "age: Input should be greater than or equal to 18",
            ],
        }

    def test_no_body(self):
        with pytest.raises(Exception) as e:
            schema.validate({})

        assert isinstance(e.value, CustomError)
        assert e.value.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "name: Field required",
                "age: Field required",
                "cnh: Field required",
            ],
        }
