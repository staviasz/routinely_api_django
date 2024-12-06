from main.contracts import EventBaseClass


class CreatedCustomerEvent(EventBaseClass):
    def __init__(self) -> None:
        super().__init__("CreatedCustomerEvent")


created_customer_event = CreatedCustomerEvent()
