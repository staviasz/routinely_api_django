from main import BaseController, base_validation_factory
from modules.customer import (
    NewPasswordController,
    NewPasswordValidator,
)
from modules.customer.factories.app.usecase.new_password_usecase_factory import (
    new_password_usecase_factory,
)


def new_password_controller_factory() -> BaseController:
    validator = base_validation_factory(NewPasswordValidator)
    usecase = new_password_usecase_factory()
    return NewPasswordController(validator=validator, usecase=usecase)
