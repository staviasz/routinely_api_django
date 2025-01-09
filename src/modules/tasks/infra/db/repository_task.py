import asyncio
import pytz
from asgiref.sync import sync_to_async
from main import Union_primitive_types, CustomError, NotFoundError
from modules.tasks.contracts import TaskRepositoryContract
from modules.tasks.domain import TaskEntity, Weekday

from django.utils import timezone
from django_.models.models import TaskDBModel, WeekdayDBModel


class RepositoryTask(TaskRepositoryContract):

    async def create(self, entity: TaskEntity) -> None:
        task_db = await sync_to_async(
            lambda: TaskDBModel.objects.create(
                **self.mapper_domain_to_repository(entity)
            )
        )()
        if entity.weekdays:
            weekdays_db = await self.get_weekdays(entity.weekdays)
            await sync_to_async(lambda: task_db.weekday.add(*weekdays_db))()
        return

    async def find_field(
        self, field_name: str, value: Union_primitive_types
    ) -> TaskEntity:
        try:
            task = await sync_to_async(
                lambda: TaskDBModel.objects.get(**{field_name: value})
            )()

            return await self.mapper_repository_to_domain(task)
        except Exception:
            raise CustomError(NotFoundError("Task not found."))

    async def update(self, entity: TaskEntity) -> None:
        try:
            task_db = await sync_to_async(
                lambda: TaskDBModel.objects.get(id=entity.id)
            )()
            for key, value in self.mapper_domain_to_repository(entity).items():
                setattr(task_db, key, value)
            await sync_to_async(lambda: task_db.save())()

            if entity.weekdays:
                weekdays_db = await self.get_weekdays(entity.weekdays)
                await sync_to_async(lambda: task_db.weekday.set(weekdays_db))()
            return
        except Exception:
            raise CustomError(NotFoundError("Task not found."))

    async def delete(self, field_name: str, value: Union_primitive_types) -> None:
        await sync_to_async(
            lambda: TaskDBModel.objects.filter(**{field_name: value}).delete()
        )()
        return

    async def find_tasks_by_user_id_and_month_and_year(
        self, user_id: str, month: int, year: int
    ) -> list[TaskEntity]:
        tasks = await sync_to_async(
            lambda: list(
                TaskDBModel.objects.filter(
                    customer_id=user_id,
                    datetime__month=month,
                    datetime__year=year,
                )
            )
        )()
        return await asyncio.gather(
            *(self.mapper_repository_to_domain(task) for task in tasks)
        )

    @sync_to_async
    def mapper_repository_to_domain(self, task: TaskDBModel) -> TaskEntity:
        return TaskEntity(
            {
                "id": str(task.id),
                "type": task.type,
                "name": task.name,
                "date_time": task.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                "category": task.category,
                "description": task.description,
                "finally_datetime": (
                    task.finally_datetime.strftime("%Y/%m/%d %H:%M:%S")
                    if task.finally_datetime
                    else None
                ),
                "weekdays": [day.name.lower() for day in task.weekday.all()] or None,
                "user_id": str(task.customer_id),
            }
        )

    @sync_to_async
    def get_weekdays(self, days: list[Weekday]) -> list[WeekdayDBModel]:
        weekdays = WeekdayDBModel.objects.filter(
            name__in=[day.capitalize() for day in days]
        )
        return weekdays

    def mapper_domain_to_repository(self, entity: TaskEntity) -> dict:
        return {
            "id": entity.id,
            "type": entity.type,
            "name": entity.name,
            "description": entity.description,
            "datetime": timezone.make_aware(entity.date_time, pytz.UTC),
            "category": entity.category,
            "finally_datetime": (
                timezone.make_aware(entity.finally_datetime, pytz.UTC)
                if entity.finally_datetime
                else None
            ),
            "customer_id": entity.user_id,
        }
