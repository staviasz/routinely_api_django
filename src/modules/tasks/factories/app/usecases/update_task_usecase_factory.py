from modules.tasks import UpdateTaskUsecaseContract, UpdateTaskUsecase
from modules.tasks.factories.db.repository_task_factory import repository_task_factory


def update_task_usecase_factory() -> UpdateTaskUsecaseContract:
    repository = repository_task_factory()
    return UpdateTaskUsecase(repository=repository)
