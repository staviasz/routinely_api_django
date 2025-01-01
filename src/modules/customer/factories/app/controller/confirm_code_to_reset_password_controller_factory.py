from main import BaseController, base_validation_factory
from modules.customer import (
    ConfirmCodeToResetPasswordController,
    ConfirmCodeToResetPasswordSchema,
)
from modules.customer.factories.app.usecase.confirm_code_to_reset_password_usecase_factory import (
    confirm_code_to_reset_password_usecase_factory,
)


def confirm_code_to_reset_password_controller_factory() -> BaseController:
    validator = base_validation_factory(ConfirmCodeToResetPasswordSchema)
    usecase = confirm_code_to_reset_password_usecase_factory()
    return ConfirmCodeToResetPasswordController(validator=validator, usecase=usecase)
