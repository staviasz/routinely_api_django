from main.contracts import (
    FindFieldOrNoneContract,
    CreateContract,
    FindFieldContract,
    UpdateContract,
)
from modules.customer.domain import CustomerAggregate

T = CustomerAggregate


class RegisterRepositoryContract(FindFieldOrNoneContract[T], CreateContract[T]):
    pass


class LoginRepositoryContract(FindFieldContract[T]):
    pass


class ForgetPasswordRepositoryContract(FindFieldContract[T]):
    pass


class ConfirmCodeToResetPasswordRepositoryContract(
    FindFieldContract[T], UpdateContract[T]
):
    pass


class NewPasswordRepositoryContract(FindFieldContract[T], UpdateContract[T]):
    pass


class CustomerRepositoryContract(
    RegisterRepositoryContract,
    LoginRepositoryContract,
    ForgetPasswordRepositoryContract,
    ConfirmCodeToResetPasswordRepositoryContract,
    NewPasswordRepositoryContract,
):
    pass
