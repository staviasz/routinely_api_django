from modules.tasks import DeleteTaskUsecaseContract, DeleteTaskUsecase
from modules.tasks.factories.db.repository_task_factory import repository_task_factory


def delete_task_usecase_factory() -> DeleteTaskUsecaseContract:
    repository = repository_task_factory()
    return DeleteTaskUsecase(repository=repository)
