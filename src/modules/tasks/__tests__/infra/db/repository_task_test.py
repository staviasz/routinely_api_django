import pytest
from django_.models.models import TaskDBModel
from main.errors.shared.custom_error import CustomError
from modules.tasks import repository_task_factory, TaskModel, TaskEntity
from asgiref.sync import sync_to_async


customer_id = "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0"
repository = repository_task_factory()
data: TaskModel = {
    "user_id": customer_id,
    "type": "task",
    "name": "task",
    "date_time": "2026/01/01 00:00",
    "category": "career",
    "description": "task",
}
entity = TaskEntity(data)


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_database")
@pytest.mark.parametrize(
    "fake_customer_db",
    [{"id": customer_id, "email": "testTask@test.com"}],
    indirect=True,
)
class TestRepositoryTask:
    def setup_method(self):
        self.data = data
        self.entity = entity
        self.repository = repository

    async def test_create_task_without_optional_fields(self, fake_customer_db):
        await self.repository.create(self.entity)
        task = await sync_to_async(
            lambda: TaskDBModel.objects.filter(id=self.entity.id).first()
        )()
        weekday = await sync_to_async(lambda: list(task.weekday.all()))()

        excepted_result = {
            "id": str(task.id),
            "user_id": str(task.customer_id),
            "type": task.type,
            "name": task.name,
            "description": task.description,
            "weekdays": weekday or None,
            "date_time": task.datetime.replace(tzinfo=None),
            "category": task.category,
            "finally_datetime": task.finally_datetime,
        }
        assert excepted_result == {**self.entity.to_dict()}

    async def test_create_task_with_optional_fields(self, fake_customer_db):
        new_entity = TaskEntity(
            {
                **self.data,
                "date_time": "2026/01/01",
                "weekdays": ["monday"],
                "finally_datetime": "2026/02/01",
            }
        )

        await self.repository.create(new_entity)
        task = await sync_to_async(
            lambda: TaskDBModel.objects.prefetch_related("weekday")
            .filter(id=new_entity.id)
            .first()
        )()
        weekday = [day.name.lower() for day in task.weekday.all()]

        excepted_result = {
            "id": str(task.id),
            "user_id": str(task.customer_id),
            "type": task.type,
            "name": task.name,
            "description": task.description,
            "weekdays": weekday or None,
            "date_time": task.datetime.replace(tzinfo=None),
            "category": task.category,
            "finally_datetime": task.finally_datetime.replace(tzinfo=None),
        }
        print(excepted_result)
        print(new_entity.to_dict())
        assert excepted_result == new_entity.to_dict()

    async def test_find_field_raise_error_if_field_not_exist(self, fake_customer_db):
        with pytest.raises(CustomError) as e:
            await self.repository.find_field("id", customer_id)

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Task not found."],
        }

    async def test_find_field(self, fake_customer_db):
        await self.repository.create(self.entity)
        task_db = await sync_to_async(
            lambda: TaskDBModel.objects.get(id=self.entity.id)
        )()

        task = await self.repository.find_field("id", self.entity.id)

        expected_task = await self.repository.mapper_repository_to_domain(task_db)
        print(task.to_dict())
        print(expected_task.to_dict())
        print(self.entity.to_dict())
        assert expected_task.to_dict() == task.to_dict() == self.entity.to_dict()

    async def test_update_task_raise_error_if_field_not_exist(self, fake_customer_db):
        with pytest.raises(CustomError) as e:
            await self.repository.update(self.entity)

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Task not found."],
        }

    async def test_update_task(self, fake_customer_db):
        await self.repository.create(self.entity)
        data_updated = TaskEntity(
            {
                **self.entity.to_dict(),
                "name": "task updated",
                "date_time": "2026/01/01",
                "weekdays": ["sunday"],
                "finally_datetime": "2026/02/01",
            }
        )
        await self.repository.update(data_updated)
        task_db = await sync_to_async(
            lambda: TaskDBModel.objects.get(id=self.entity.id)
        )()

        task = await self.repository.find_field("id", self.entity.id)

        expected_task = await self.repository.mapper_repository_to_domain(task_db)
        assert expected_task.to_dict() == task.to_dict() == data_updated.to_dict()

    async def test_delete_task(self, fake_customer_db):
        await self.repository.create(self.entity)
        await self.repository.delete("id", self.entity.id)
        with pytest.raises(CustomError) as e:
            await self.repository.find_field("id", self.entity.id)
        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 404,
            "messages_error": ["Task not found."],
        }

    async def test_find_tasks_by_user_id_and_month_and_year(
        self, fake_customer_db
    ) -> None:
        arrange: list[TaskEntity] = [
            TaskEntity(
                {
                    "name": "task 1",
                    "category": "career",
                    "user_id": customer_id,
                    "date_time": "2026/01/01",
                    "description": "task 1",
                    "type": "task",
                }
            ),
            TaskEntity(
                {
                    "name": "task 2",
                    "category": "career",
                    "user_id": customer_id,
                    "date_time": "2026/01/01",
                    "description": "task 2",
                    "type": "task",
                }
            ),
            TaskEntity(
                {
                    "name": "task 3",
                    "category": "career",
                    "user_id": customer_id,
                    "date_time": "2026/02/01",
                    "description": "task 3",
                    "type": "task",
                }
            ),
        ]
        for task in arrange:
            await self.repository.create(task)

        tasks = await self.repository.find_tasks_by_user_id_and_month_and_year(
            customer_id, 1, 2026
        )
        assert len(tasks) == 2

        tasks = await self.repository.find_tasks_by_user_id_and_month_and_year(
            customer_id, 2, 2026
        )
        assert len(tasks) == 1
