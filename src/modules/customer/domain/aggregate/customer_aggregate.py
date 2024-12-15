from main.domain.aggregates import Aggregate
from main.errors.shared.custom_error import CustomError
from modules.customer.domain import (
    InputCustomerAggregateModel,
    AccountEntity,
    CustomerEntity,
)
from modules.customer.domain.aggregate.value_objects.password_value_object import (
    PasswordValueObject,
)


class CustomerAggregate(Aggregate):

    def __init__(self, props: InputCustomerAggregateModel) -> None:
        self._validate(props)
        self.__props = props
        self.name = props.get("name", "")
        self.email = props.get("email", "")
        self.password = props.get("password", "")
        self.accepted_terms = props.get("accepted_terms", False)
        self.is_active = props.get("is_active", False)

    def _validate(self, props: InputCustomerAggregateModel) -> None:
        self._clear_errors()

        self._create_id(props.get("id"), "CustomerAggregate")

        props_customer = {
            "id": self.id,
            "name": props.get("name", ""),
            "accepted_terms": props.get("accepted_terms", False),
        }

        props_account = {
            "id": self.id,
            "email": props.get("email", ""),
            "password": props.get("password", ""),
        }

        self._validate_entities(
            [
                {"entity": CustomerEntity, "props": props_customer},
                {"entity": AccountEntity, "props": props_account},
            ]
        )
        self._raize_errors()

        props["is_active"] = False if not props.get("id") else props["is_active"]

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_password(self, password: str) -> None:
        new_password = PasswordValueObject(password)
        self.password = new_password.value
