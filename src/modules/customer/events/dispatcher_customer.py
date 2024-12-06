from main.infra import DispatcherEvents
from modules.customer.events.events_customer import created_customer_event
from modules.customer.events.handles_customer import (
    send_email_register_customer_handler,
)


class DispatcherCustomer(DispatcherEvents):
    pass


dispatcher_customer = DispatcherCustomer()

dispatcher_customer.register(
    created_customer_event.get_name(), send_email_register_customer_handler
)
