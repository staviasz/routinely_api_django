from main import BaseController, base_validation_factory
from modules.customer import (
    ForgetPasswordController,
    ForgetPasswordSchema,
)
from modules.customer.factories.app.usecase.forget_password_usecase_factory import (
    forget_password_usecase_factory,
)


def forget_password_controller_factory() -> BaseController:
    validator = base_validation_factory(ForgetPasswordSchema)
    usecase = forget_password_usecase_factory()
    return ForgetPasswordController(validator=validator, usecase=usecase)
