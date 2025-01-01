from modules.customer import CustomerRepositoryContract, RepositoryCustomer


def repository_customer_factory() -> CustomerRepositoryContract:
    return RepositoryCustomer()
