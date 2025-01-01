from modules.tasks import ListTasksUsecaseContract, ListTaskUsecase
from modules.tasks.factories.db.repository_task_factory import repository_task_factory


def list_task_usecase_factory() -> ListTasksUsecaseContract:
    repository = repository_task_factory()
    return ListTaskUsecase(repository=repository)
