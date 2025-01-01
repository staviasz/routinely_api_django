from main import BaseController, base_validation_factory
from modules.tasks.factories.app.usecases.create_task_usecase_factory import (
    create_task_usecase_factory,
)
from modules.tasks import CreateTaskSchema, CreateTaskController


def create_task_controller_factory() -> BaseController:
    validator = base_validation_factory(CreateTaskSchema)
    usecase = create_task_usecase_factory()
    return CreateTaskController(validator=validator, usecase=usecase)
