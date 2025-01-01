from main import BaseController, base_validation_factory
from modules.tasks.factories.app.usecases.delete_task_usecase_factory import (
    delete_task_usecase_factory,
)
from modules.tasks import DeleteTaskController, DeleteTaskSchema


def delete_task_controller_factory() -> BaseController:
    validator = base_validation_factory(DeleteTaskSchema)
    usecase = delete_task_usecase_factory()
    return DeleteTaskController(validator=validator, usecase=usecase)
