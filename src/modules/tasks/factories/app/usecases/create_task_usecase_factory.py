from modules.tasks import CreateTaskUsecaseContract, CreateTaskUsecase
from modules.tasks.factories.db.repository_task_factory import repository_task_factory


def create_task_usecase_factory() -> CreateTaskUsecaseContract:
    repository = repository_task_factory()
    return CreateTaskUsecase(repository=repository)
