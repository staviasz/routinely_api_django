from main.infra import DispatcherEvents
from modules.customer.events.events_customer import (
    created_customer_event,
    forgot_password_event,
)
from modules.customer.events.handles_customer import (
    send_email_register_customer_handler,
    send_email_forgot_password_customer_handler,
)


class DispatcherCustomer(DispatcherEvents):
    pass


dispatcher_customer = DispatcherCustomer()

dispatcher_customer.register(
    created_customer_event.get_name(), send_email_register_customer_handler
)
dispatcher_customer.register(
    forgot_password_event.get_name(), send_email_forgot_password_customer_handler
)
