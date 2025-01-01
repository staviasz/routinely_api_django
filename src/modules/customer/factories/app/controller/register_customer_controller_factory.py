from main import base_validation_factory
from modules.customer import (
    RegisterCustomerController,
    RegisterCustomerSchema,
    register_customer_usecase_factory,
)


def register_customer_controller_factory() -> RegisterCustomerController:
    validator = base_validation_factory(RegisterCustomerSchema)
    usecase = register_customer_usecase_factory()
    return RegisterCustomerController(validator=validator, usecase=usecase)
