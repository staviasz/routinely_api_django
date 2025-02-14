from main import BaseController, base_validation_factory
from modules.customer import (
    ConfirmEmailController,
    ConfirmEmailSchema,
    EncryptionToSendEmailAdapter,
)
from modules.customer.factories.app.usecase.confirm_email_usecase_factory import (
    confirm_email_usecase_factory,
)


def confirm_email_controller_factory() -> BaseController:
    validator = base_validation_factory(ConfirmEmailSchema)
    usecase = confirm_email_usecase_factory()
    crypto = EncryptionToSendEmailAdapter()
    return ConfirmEmailController(validator=validator, usecase=usecase, crypto=crypto)
