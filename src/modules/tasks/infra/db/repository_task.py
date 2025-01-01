from main import Union_primitive_types
from modules.tasks import TaskRepositoryContract, TaskEntity


class RepositoryTask(TaskRepositoryContract):
    def __init__(self, db_client) -> None:
        self.db_client = db_client

    async def create(self, entity: TaskEntity) -> None:
        return

    async def find_field(
        self, field_name: str, value: Union_primitive_types
    ) -> TaskEntity:
        return await self.db_client.find_field(field_name, value)

    async def update(self, entity: TaskEntity) -> None:
        return

    async def delete(self, field_name: str, value: Union_primitive_types) -> None:
        return

    async def find_tasks_by_user_id_and_month_and_year(
        self, user_id: str, month: int, year: int
    ):
        return await self.db_client.find_tasks_by_user_id_and_month_and_year(
            user_id, month, year
        )
