from main import BaseController, base_validation_factory
from modules.tasks.factories.app.usecases.update_task_usecase_factory import (
    update_task_usecase_factory,
)
from modules.tasks import UpdateTaskController, UpdateTaskSchema


def update_task_controller_factory() -> BaseController:
    validator = base_validation_factory(UpdateTaskSchema)
    usecase = update_task_usecase_factory()
    return UpdateTaskController(validator=validator, usecase=usecase)
