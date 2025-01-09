import pytest
from asgiref.sync import sync_to_async
from modules.auth import repository_session_factory, SessionEntity, SessionModel
from django_.models.models import SessionDBModel


repository = repository_session_factory()
customer_id = "92c2fd60-65cc-4c0a-9f5c-1e9cb1584af0"
data: SessionModel = {"user_id": customer_id}

entity = SessionEntity(data)


@pytest.mark.asyncio
@pytest.mark.usefixtures("setup_database")
@pytest.mark.parametrize("fake_customer_db", [customer_id], indirect=True)
class TestRepositorySession:
    def setup_method(self):
        self.repository = repository
        self.entity = entity
        self.data = data
        self.customer_id = customer_id

    async def test_create_session(self, fake_customer_db):
        await self.repository.create(self.entity)
        session = await sync_to_async(
            lambda: SessionDBModel.objects.get(id=self.entity.id)
        )()

        expected_session = {
            **self.repository._mapper_repository_to_domain(session).to_dict(),
            "expires_at": session.expires_at.replace(tzinfo=None),
            "created_at": session.created_at.replace(tzinfo=None),
        }
        assert expected_session == self.entity.to_dict()

    async def test_find_session_or_none(self, fake_customer_db):
        session = await self.repository.find_session_or_none(self.customer_id)
        assert session is None

        await self.repository.create(self.entity)
        session = await self.repository.find_session_or_none(self.customer_id)

        expected_session = {
            **session.to_dict(),
            "expires_at": session.expires_at.replace(tzinfo=None),
            "created_at": session.created_at.replace(tzinfo=None),
        }
        assert expected_session == self.entity.to_dict()
