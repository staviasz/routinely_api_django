import os
import django
import pytest
from pathlib import Path
from django.db import connections
from django.core.management import call_command
from django.conf import settings
import asyncio


if not settings.configured:
    django.setup()

from modules.auth.factories.services.create_session_service_factory import (
    create_session_service_factory,
)
from django_.models.models import CustomerDBModel, AccountDBModel, SessionDBModel


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


@pytest.fixture(scope="function")
def fake_customer_logged():
    customer_data = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "john@doe.com",
        "password": "@Teste123",
        "accepted_terms": True,
        "name": "John Doe",
        "is_active": True,
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

    session = asyncio.run(
        create_session_service_factory().handle(
            {"user_id": customer.id, "email": customer_data["email"]}
        )
    )

    yield session

    customer.delete()
    account.delete()
    SessionDBModel.objects.all().delete()
