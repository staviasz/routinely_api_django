from main.domain.aggregates import Aggregate
from modules.customer.domain import (
    InputCustomerAggregateModel,
    AccountEntity,
    CustomerEntity,
)


class CustomerAggregate(Aggregate):
    def __init__(self, props: InputCustomerAggregateModel) -> None:
        self._validate(props)

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

        self.to_dict = {
            **props_customer,
            "account": props_account,
        }
