from django.utils import timezone
from asgiref.sync import sync_to_async
import pytz
from modules.auth import SessionRepositoryContract, SessionEntity
from django_.models.models import SessionDBModel


class RepositorySession(SessionRepositoryContract):

    async def create(self, entity: SessionEntity) -> None:
        await sync_to_async(
            lambda: SessionDBModel.objects.create(
                **self._mapper_domain_to_repository(entity)
            )
        )()
        return

    async def find_session_or_none(self, user_id: str) -> SessionEntity | None:
        session = await sync_to_async(
            lambda: SessionDBModel.objects.filter(customer_id=user_id).last()
        )()
        return self._mapper_repository_to_domain(session) if session else None

    def _mapper_domain_to_repository(self, entity: SessionEntity) -> dict:
        return {
            "id": entity.id,
            "customer_id": entity.user_id,
            "created_at": timezone.make_aware(entity.created_at, pytz.UTC),
            "expires_at": timezone.make_aware(entity.expires_at, pytz.UTC),
        }

    def _mapper_repository_to_domain(self, session: SessionDBModel) -> SessionEntity:
        return SessionEntity(
            {
                "id": str(session.id),
                "user_id": str(session.customer_id),
                "created_at": session.created_at,
                "expires_at": session.expires_at,
            }
        )
