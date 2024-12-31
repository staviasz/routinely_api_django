import pytest

from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.tasks import CreateTaskUsecase, TaskEntity


class CreateTaskRepositoryInMemory(RepositoryInMemory[TaskEntity]):
    pass


@pytest.mark.asyncio
class TestCreateTaskUsecase:
    def setup_method(self):
        self.repository = CreateTaskRepositoryInMemory()
        self.usecase = CreateTaskUsecase(self.repository)
        self.data = {
            "user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b",
            "type": "task",
            "category": "career",
            "name": "Teste",
            "date_time": "2023/01/01",
            "description": "Teste",
        }

    async def test_entity_errors(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The user_id in TaskEntity is invalid.",
                "The Type must be one of: task, habit",
                "The category must be one of: career, finance, study, health, leisure, productivity, miscellaneous",
                "The name is mandatory and must be up to 50 characters long",
                "The date_time is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS",
                "The Description is mandatory and must be up to 1000 characters long",
            ],
        }

    async def test_perform(self):
        assert len(self.repository.list_data) == 0

        result = await self.usecase.perform(self.data)

        assert len(self.repository.list_data) == 1
        assert self.repository.list_data[0].user_id == self.data["user_id"]
        assert self.repository.list_data[0].id == result["id"]
