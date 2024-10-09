from main.domain.aggregates import Aggregate
from modules.customer.domain import (
    InputCustomerAggregateModel,
    AccountEntity,
    CustomerEntity,
)


class CustomerAggregate(Aggregate):
    def __init__(self, props: InputCustomerAggregateModel) -> None:
        self._validate(props)
        self.__props = props

    @property
    def name(self) -> str:
        return self.__props["name"]

    @property
    def accepted_terms(self) -> bool:
        return self.__props["accepted_terms"]

    @property
    def email(self) -> str:
        return self.__props["email"]

    @property
    def password(self) -> str:
        return self.__props["password"]

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
