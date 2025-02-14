from modules.auth.factories.services.create_session_service_factory import (
    create_session_service_factory,
)
from modules.auth.types.session_type import SessionOutput
from modules.customer.factories.infra.db.repository_customer_factory import (
    repository_customer_factory,
)

repository = repository_customer_factory()


async def get_tokens(email: str) -> SessionOutput:
    user = await repository.find_field("email", email)
    return await create_session_service_factory().handle({"user_id": user.id})
