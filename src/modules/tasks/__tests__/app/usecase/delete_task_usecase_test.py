import pytest

from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.tasks import DeleteTaskUsecase, TaskEntity


class DeleteTaskRepositoryInMemory(RepositoryInMemory[TaskEntity]):
    pass


@pytest.mark.asyncio
class TestDeleteTaskUsecase:
    def setup_method(self):
        self.repository = DeleteTaskRepositoryInMemory()
        self.usecase = DeleteTaskUsecase(self.repository)
        self.data = {
            "user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b",
            "type": "task",
            "category": "career",
            "name": "Teste",
            "date_time": "2023/01/01",
            "description": "Teste",
        }
        self.entity = TaskEntity(self.data)

    async def test_perform(self):
        self.repository.list_data.append(self.entity)

        await self.usecase.perform({"id": self.entity.id})

        assert len(self.repository.list_data) == 0
