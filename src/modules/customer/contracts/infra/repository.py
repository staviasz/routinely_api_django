from main.contracts import FindFieldOrNoneContract, CreateContract, FindFieldContract
from modules.customer.domain import CustomerAggregate

T = CustomerAggregate


class RegisterRepositoryContract(FindFieldOrNoneContract[T], CreateContract[T]):
    pass


class LoginRepositoryContract(FindFieldContract[T]):
    pass


class CustomerRepositoryContract(RegisterRepositoryContract, LoginRepositoryContract):
    pass
