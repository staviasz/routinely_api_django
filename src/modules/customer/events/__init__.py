from .events_customer import (
    CreatedCustomerEvent,
    ForgotPasswordEvent,
)
from .handles_customer import (
    send_email_register_customer_handler,
    send_email_forgot_password_customer_handler,
)

from .dispatcher_customer import dispatcher_customer
