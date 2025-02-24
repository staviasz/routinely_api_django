import asyncio
import pytest
from main import RequestClient
from main.__tests__ import await_pending_tasks, get_tokens
from modules.customer import (
    repository_customer_factory,
)
from modules.customer.infra.cache.cache import Cache
from modules.customer.infra.crypto.encryption_to_send_email import (
    EncryptionToSendEmailAdapter,
)


@pytest.mark.usefixtures("setup_database")
class Teste2e:

    data_by_method: dict = {}

    def setup_class(cls):
        cls.cache = Cache()
        cls.client = RequestClient()
        cls.data = {
            "name": "Test",
            "accepted_terms": True,
            "email": "test@example.com",
            "password": "@Teste123",
            "confirmed_password": "@Teste123",
        }
        cls.repository = repository_customer_factory()

    def test_create_customer(self):
        response = self.client.post(
            {
                "path": "/customer/?callback_url=http://127.0.0.1:3000",
                "data": self.data,
            }
        )
        assert response.status_code == 201
        await_pending_tasks()

    def test_confirm_email(self):
        email_customer = self.data["email"]
        callback_url = "http://localhost:3000"
        crypto = EncryptionToSendEmailAdapter()

        str_crypto = f"{crypto.encrypt(f"{email_customer}--{callback_url}")}"
        response = self.client.get({"path": f"/customer/confirm-email/?{str_crypto}"})

        assert response.status_code == 302
        assert response.headers["Location"] == callback_url

    def test_login_customer(self):
        response = self.client.post(
            {
                "path": "/customer/auth/",
                "data": {
                    "email": self.data["email"],
                    "password": self.data["password"],
                },
            }
        )
        response_dict = response.json()
        assert response.status_code == 200
        assert isinstance(response_dict["access_token"], str)
        assert isinstance(response_dict["expires_in"], int)
        assert isinstance(response_dict["refresh_token"], str)

    def test_refresh_login_customer_with_valid_token(self):

        tokens = asyncio.run(get_tokens(self.data["email"]))

        response = self.client.post(
            {
                "path": "/customer/refresh-auth/",
                "data": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                },
            }
        )
        response_dict = response.json()
        assert response.status_code == 200
        assert isinstance(response_dict["access_token"], str)
        assert isinstance(response_dict["expires_in"], int)
        assert isinstance(response_dict["refresh_token"], str)

    def test_forgot_password(self):
        response = self.client.post(
            {
                "path": "/customer/forgot-password/",
                "data": {"email": self.data["email"]},
            }
        )
        self.data_by_method["account_id"] = response.json()["account_id"]
        assert response.status_code == 200
        assert isinstance(self.data_by_method["account_id"], str)

    def test_confirm_code(self):
        self.cache.set(
            self.data["email"],
            "123456",
        )

        response = self.client.post(
            {
                "path": "/customer/confirm-code/",
                "data": {
                    "account_id": self.data_by_method["account_id"],
                    "code": "123456",
                },
            }
        )
        assert response.status_code == 204

    def test_new_password(self):
        response = self.client.post(
            {
                "path": "/customer/new-password/",
                "data": {
                    "account_id": self.data_by_method["account_id"],
                    "password": "@Update123",
                    "confirm_password": "@Update123",
                },
            }
        )
        assert response.status_code == 204
