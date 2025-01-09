from django.db import migrations
import uuid

DAYS_WEEK = [
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
]


def create_weekdays(apps, schema_editor):
    WeekdayDBModel = apps.get_model("models", "WeekdayDBModel")
    for day in DAYS_WEEK:
        WeekdayDBModel.objects.get_or_create(id=uuid.uuid4(), name=day[0])


class Migration(migrations.Migration):
    dependencies = [
        ("models", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_weekdays),
    ]
