from unittest import mock
import pytest
from main.errors.shared import (
    CustomErrorAbstract,
    InputObjectErrorType,
    CustomError,
)


class ConcreteCustomError(CustomErrorAbstract):
    def __init__(self, inputObjectError: InputObjectErrorType) -> None:
        super().__init__(
            inputObjectError["code_error"], inputObjectError["message_error"]
        )


class TestCustomErrorAbstract:

    def test_init_props(self):
        instance = ConcreteCustomError(
            {"code_error": 404, "message_error": "Not Found"}
        )

        assert instance.code_error == 404
        assert instance.message_error == "Not Found"


class TestCustomError:

    def setup_method(self):
        self.error_props_1 = {
            "code_error": 500,
            "message_error": "Internal Server Error",
        }
        self.error_props_2 = {
            "code_error": 400,
            "message_error": "Bad Request",
        }

        self.custom_error_instance_1 = ConcreteCustomError(self.error_props_1)

        self.custom_error_instance_2 = ConcreteCustomError(self.error_props_2)

    def test_single_instance(self):
        custom_error = CustomError(self.custom_error_instance_1)

        assert len(custom_error.errors) == 1
        assert custom_error.errors[0].code_error == 500
        assert custom_error.errors[0].message_error == "Internal Server Error"

        formatted = custom_error.formated_errors
        assert formatted["code_error"] == 500
        assert formatted["messages_error"] == ["Internal Server Error"]

    def test_list_of_instances(self):
        custom_error = CustomError(
            [self.custom_error_instance_1, self.custom_error_instance_2]
        )

        assert len(custom_error.errors) == 2
        assert custom_error.errors[0].code_error == 500
        assert custom_error.errors[1].code_error == 400

        formatted = custom_error.formated_errors
        assert formatted["code_error"] == 500
        assert formatted["messages_error"] == [
            "Internal Server Error",
            "Bad Request",
        ]

    def test_invalid_construction(self):
        with pytest.raises(TypeError):
            CustomError("Invalid Error")  # Deve lançar TypeError

        with pytest.raises(TypeError):
            CustomError([self.custom_error_instance_1, "Invalid Error"])
