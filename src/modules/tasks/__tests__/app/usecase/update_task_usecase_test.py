import pytest

from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.tasks import UpdateTaskUsecase, TaskEntity


class UpdateTaskRepositoryInMemory(RepositoryInMemory[TaskEntity]):
    pass


@pytest.mark.asyncio
class TestUpdateTaskUsecase:
    def setup_method(self):
        self.repository = UpdateTaskRepositoryInMemory()
        self.usecase = UpdateTaskUsecase(self.repository)
        self.data = {
            "user_id": "811c5f65-c4e1-4084-8b15-e8342de5d57b",
            "type": "tasks",
            "category": "career",
            "name": "Teste",
            "date_time": "2023/01/01",
            "description": "Teste",
        }
        self.entity = TaskEntity(self.data)

    async def test_not_found_id(self):
        with pytest.raises(CustomError) as e:
            await self.usecase.perform({"id": self.entity.id})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["id not found."],
        }

    async def test_entity_errors(self):
        self.repository.list_data.append(self.entity)

        with pytest.raises(CustomError) as e:
            await self.usecase.perform(
                {
                    "id": self.entity.id,
                    "category": "test",
                    "description": " ",
                    "name": " ",
                    "type": "test",
                    "date_time": "test",
                }
            )

        custom_error = e.value
        print(custom_error.formate_errors)
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": [
                "The Type must be one of: tasks, habit",
                "The category must be one of: career, finance, study, health, leisure, productivity, miscellaneous",
                "The name is mandatory and must be up to 50 characters long",
                "The date_time is mandatory and must be in the formats YYYY/mm/dd, YYYY/mm/dd HH:MM, YYYY/mm/dd HH:MM:SS, YYYY/mm/ddTHH:MM:SS",
                "The Description is mandatory and must be up to 1000 characters long",
            ],
        }

        assert self.repository.list_data[0] == self.entity

    async def test_perform(self):
        self.repository.list_data.append(self.entity)

        await self.usecase.perform(
            {
                "id": self.entity.id,
                "description": "Teste Update",
                "name": "Teste Update",
            }
        )

        repo_entity = self.repository.list_data[0]
        assert repo_entity != self.entity
        assert repo_entity.description == "Teste Update"
        assert repo_entity.name == "Teste Update"
