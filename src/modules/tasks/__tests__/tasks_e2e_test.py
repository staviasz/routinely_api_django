import pytest

from main.configs.config_test_server import RequestClient
from modules.tasks.factories.db.repository_task_factory import repository_task_factory


@pytest.mark.usefixtures("setup_database")
@pytest.mark.usefixtures("fake_customer_logged")
class TestTasksE2E:
    def setup_class(cls):
        cls.client = RequestClient()
        cls.data = {
            "name": "Testing Task",
            "description": "description Task",
            "type": "task",
            "date_time": "2030/01/01 20:05:50",
            "category": "career",
            "weekdays": ["monday", "tuesday", "wednesday", "thursday"],
            "finally_datetime": "2030/02/01 20:05:50",
        }
        cls.repository = repository_task_factory()

    def test_create_task_without_session(self):
        response = self.client.post(
            {
                "path": "/task/",
                "data": self.data,
            }
        )
        assert response.status_code == 401
        assert response.json()["message"] == "Token not found"

    def test_create_task(self, fake_customer_logged):
        session = fake_customer_logged
        response = self.client.post(
            {
                "path": "/task/",
                "data": self.data,
                "headers": {"Authorization": f"Bearer {session["access_token"]}"},
            }
        )
        assert response.status_code == 201

    def test_get_tasks(self, fake_customer_logged):
        session = fake_customer_logged
        response = self.client.get(
            {
                "path": "/task/",
                "headers": {"Authorization": f"Bearer {session['access_token']}"},
            }
        )
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_update_task(self, fake_customer_logged):
        session = fake_customer_logged
        response_create = self.client.post(
            {
                "path": "/task/",
                "data": self.data,
                "headers": {"Authorization": f"Bearer {session['access_token']}"},
            }
        )
        id = response_create.json()["id"]
        response = self.client.put(
            {
                "path": f"/task/{id}/",
                "data": self.data,
                "headers": {"Authorization": f"Bearer {session['access_token']}"},
            }
        )
        assert response.status_code == 204

    def test_delete_task(self, fake_customer_logged):
        session = fake_customer_logged
        response_create = self.client.post(
            {
                "path": "/task/",
                "data": self.data,
                "headers": {"Authorization": f"Bearer {session['access_token']}"},
            }
        )
        id = response_create.json()["id"]
        response = self.client.delete(
            {
                "path": f"/task/{id}/",
                "headers": {"Authorization": f"Bearer {session['access_token']}"},
            }
        )
        assert response.status_code == 204
