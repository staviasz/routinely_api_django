from modules.tasks import TaskRepositoryContract, RepositoryTask


def repository_task_factory() -> TaskRepositoryContract:
    return RepositoryTask()
