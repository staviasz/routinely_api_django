from modules.customer import CustomerRepositoryContract, RepositoryCustomer
from modules.customer.infra.crypto.encryption_to_repository import (
    EncryptionToRepositoryAdapter,
)


def repository_customer_factory() -> CustomerRepositoryContract:
    cripto = EncryptionToRepositoryAdapter()
    return RepositoryCustomer(cripto=cripto)
