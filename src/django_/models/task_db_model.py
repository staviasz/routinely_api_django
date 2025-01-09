from django.db import models


TaskCategories = (
    "career",
    "finance",
    "study",
    "health",
    "leisure",
    "productivity",
    "miscellaneous",
)

TaskType = ("task", "habit")
Weekday = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)

DAYS_WEEK = [(t, t) for t in Weekday]


class WeekdayDBModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100, choices=DAYS_WEEK, null=False, unique=True)


TYPES_TASK = [(t, t) for t in TaskType]
CATEGORIES_TASK = [(t, t) for t in TaskCategories]


class TaskDBModel(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.CharField(max_length=100, choices=TYPES_TASK, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    weekday = models.ManyToManyField(WeekdayDBModel, related_name="task")
    datetime = models.DateTimeField(null=False)
    category = models.CharField(max_length=100, choices=CATEGORIES_TASK, null=False)
    finally_datetime = models.DateTimeField(null=True)
    customer = models.ForeignKey(
        "CustomerDBModel", on_delete=models.CASCADE, null=False
    )
