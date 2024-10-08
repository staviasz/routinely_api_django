from main.domain.entity import Entity
from main.errors import FieldIsRequiredError
from modules.customer.domain import (
    NameValueObject,
    InvalidAcceptedTermsError,
    InputCustomerEntityModel,
)


class CustomerEntity(Entity[InputCustomerEntityModel]):
    def __init__(self, __props: InputCustomerEntityModel) -> None:
        self._validate(__props)
        self.__props = __props

    @property
    def name(self) -> str:
        return self.__props["name"]

    @property
    def accepted_terms(self) -> bool:
        return self.__props["accepted_terms"]

    def _validate(self, props: InputCustomerEntityModel) -> None:
        self._clear_errors()

        self._create_id(props.get("id"), "CustomerEntity")
        self._validate_value_objects(
            [{"value_object": NameValueObject, "props": props.get("name", "")}]
        )

        self.__accepted_terms(props.get("accepted_terms", False))
        self._raize_errors()

    def __accepted_terms(self, accepted_terms: bool) -> None:
        if not isinstance(accepted_terms, bool):
            self._add_error(FieldIsRequiredError("accepted_terms"))
        elif not accepted_terms:
            self._add_error(InvalidAcceptedTermsError())
        return
