from main import BaseController, base_validation_factory
from modules.customer import LoginController, LoginValidator
from modules.customer.factories.app.usecase.login_usecase_factory import (
    login_usecase_factory,
)


def login_controller_factory() -> BaseController:
    validator = base_validation_factory(LoginValidator)
    usecase = login_usecase_factory()
    return LoginController(validator=validator, usecase=usecase)
