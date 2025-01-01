from main import BaseController, base_validation_factory
from modules.customer import (
    RefreshLoginController,
    RefreshLoginSchema,
)
from modules.customer.factories.app.usecase.refresh_login_usecase_factory import (
    refresh_login_usecase_factory,
)


def refresh_login_controller_factory() -> BaseController:
    validator = base_validation_factory(RefreshLoginSchema)
    usecase = refresh_login_usecase_factory()
    return RefreshLoginController(validator=validator, usecase=usecase)
