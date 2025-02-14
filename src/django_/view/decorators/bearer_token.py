import asyncio
from functools import wraps
from rest_framework.response import Response

from main.app.helpers.http_helpers import unauthorized
from modules.auth.factories.services.create_session_service_factory import (
    create_session_service_factory,
)
from modules.customer.app.errors.unauthorized import UnauthorizedError


def bearer_token(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")

        print(token)
        if not token:
            return Response(
                {"message": "Token not found"},
                status=401,
            )
        try:
            session_service = create_session_service_factory()
            payload = asyncio.run(
                session_service.verify_token(token.split("Bearer ")[1])
            )
            request.user = payload
        except Exception as e:
            print("error", e)
            return Response(
                {"message": "Invalid token"},
                status=401,
            )

        return func(self, request, *args, **kwargs)

    return wrapper
