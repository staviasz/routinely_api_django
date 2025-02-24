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
    param = request.param
    customer_data = {
        "id": param["id"],
        "email": param["email"],
        "password": param.get("password", "@Teste123"),
        "accepted_terms": param.get("accepted_terms", True),
        "name": param.get("name", "Teste"),
        "is_active": param.get("is_active", True),
    }
    customer = CustomerDBModel.objects.create(
        id=customer_data["id"],
        name=customer_data["name"],
        accepted_terms=customer_data["accepted_terms"],
    )
    account = AccountDBModel.objects.create(
        id=customer.id,
        email=customer_data["email"],
        is_active=customer_data["is_active"],
        password=customer_data["password"],
        customer=customer,
    )
    yield
    customer.delete()
    account.delete()
