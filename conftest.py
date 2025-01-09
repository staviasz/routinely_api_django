import os
import django
import pytest
from pathlib import Path
from django.db import connections
from django.core.management import call_command
from django.conf import settings


if not settings.configured:
    django.setup()

from django_.models.models import CustomerDBModel, AccountDBModel


@pytest.fixture(scope="class")
def setup_database():
    connection = connections["default"]
    connection.creation.create_test_db()
    call_command("migrate")

    yield

    connection.creation.destroy_test_db(connection.settings_dict["NAME"])


@pytest.fixture(scope="function")
def fake_customer_db(request):
    customer_id = request.param
    print(customer_id)
    customer = CustomerDBModel.objects.create(
        id=customer_id, name="test", accepted_terms=True
    )
    account = AccountDBModel.objects.create(
        id=customer.id,
        email="test@example.com",
        is_active=True,
        password="test",
        customer=customer,
    )
    yield
    customer.delete()
    account.delete()
