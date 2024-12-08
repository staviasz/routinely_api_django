from typing import cast
from main.errors import BadRequestError, CustomError
from modules.auth.services.base_session_tokens import SessionService
from modules.auth.types.session_type import SessionInput, SessionOutput


class RefreshSessionService(SessionService):

    async def handle(self, props: SessionInput) -> SessionOutput:
        tokens = props.get("tokens")
        if not tokens or "access_token" not in tokens or "refresh_token" not in tokens:
            raise CustomError(BadRequestError("Invalid access token or refresh token."))

        payload_token = self.token.decode(tokens["access_token"])
        payload_refresh_token = self.token.decode(tokens["refresh_token"])
        if payload_token["session_id"] != payload_refresh_token["session_id"]:
            raise CustomError(BadRequestError("Access token not match refresh token."))

        del payload_token["iat"]
        del payload_token["exp"]
        del payload_token["session_id"]

        return await self.create_session(cast(SessionInput, payload_token))
