from main.domain.entities.entity import Entity
from modules.customer.domain.aggregate.value_objects import (
    EmailValueObject,
    PasswordValueObject,
)
from modules.customer.domain.models import InputAccountEntityModel


class AccountEntity(Entity):
    def __init__(self, __props: InputAccountEntityModel) -> None:
        self._validate(__props)
        self.__props = __props

    @property
    def email(self) -> str:
        return self.__props.get("email")

    @property
    def password(self) -> str:
        return self.__props.get("password")

    def _validate(self, props: InputAccountEntityModel) -> None:
        self._clear_errors()

        self._create_id(props.get("id"), "AccountEntity")
        self._validate_value_objects(
            [
                {"value_object": EmailValueObject, "props": props.get("email", "")},
                {
                    "value_object": PasswordValueObject,
                    "props": props.get("password", ""),
                },
            ]
        )

        self._raize_errors()
