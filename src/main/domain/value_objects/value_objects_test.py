import pytest
from main.domain.value_objects.value_objects import (
    ValueObject,
)
from main.errors.shared import CustomErrorAbstract


class ErrorTest(CustomErrorAbstract):
    def __init__(self, message_error: str) -> None:
        super().__init__(code_error=400, message_error=message_error)


class ConcreteValueObject(ValueObject[str]):
    def __init__(self, props: str) -> None:
        self._validate(props)
        super().__init__(props)

    def _validate(self, props: str) -> None:
        self._clear_errors()
        if len(props) < 3:
            self._add_error(
                ErrorTest(
                    "O valor deve ter pelo menos 3 caracteres.",
                )
            )


class TestValueObject:

    def test_value_property(self):
        vo = ConcreteValueObject("test value")
        assert (
            vo.value == "test value"
        ), "Erro: O valor retornado pela propriedade `value` está incorreto."

    def test_errors_property(self):
        vo = ConcreteValueObject("t")
        assert vo._errors() is not None
        assert len(vo._errors()) == 1
        assert isinstance(vo._errors()[0], ErrorTest)

    def test_clear_errors(self):
        vo = ConcreteValueObject("t")
        assert vo._errors() is not None
        assert len(vo._errors()) == 1
        assert isinstance(vo._errors()[0], ErrorTest)

        vo._clear_errors()
        assert vo._errors() is None

    def test_exception_invalid_instance_in_add_error(self):
        vo = ConcreteValueObject("t")

        with pytest.raises(TypeError):
            vo._add_error("invalid_instance")
