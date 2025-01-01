from main import BaseController, base_validation_factory
from modules.tasks.factories.app.usecases.list_task_usecase_factory import (
    list_task_usecase_factory,
)
from modules.tasks import ListTaskController, ListTasksSchema


def list_task_controller_factory() -> BaseController:
    validator = base_validation_factory(ListTasksSchema)
    usecase = list_task_usecase_factory()
    return ListTaskController(validator=validator, usecase=usecase)
