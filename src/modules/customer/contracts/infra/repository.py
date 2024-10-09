from main.contracts import FindFieldOrNoneContract, CreateContract
from modules.customer.domain import CustomerAggregate

T = CustomerAggregate


class RegisterRepositoryContract(FindFieldOrNoneContract[T], CreateContract[T]):
    pass


class CustomerRepositoryContract(RegisterRepositoryContract):
    pass
