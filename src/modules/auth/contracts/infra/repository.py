from main.contracts import CreateContract, FindFieldOrNoneContract, DeleteContract
from modules.auth.domain import SessionEntity


T = SessionEntity


class CreateSessionRepositoryContract(CreateContract[T]):
    pass


class SessionRepositoryContract:
    pass
