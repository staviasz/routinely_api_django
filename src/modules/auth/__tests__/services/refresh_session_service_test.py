from datetime import datetime, timedelta
import pytest
from main.errors.shared.custom_error import CustomError
from main.infra.repository.repository_in_memory import RepositoryInMemory
from modules.auth import SessionEntity, JWTAdapter, RefreshSessionService


class SessionRepositoryInMemory(RepositoryInMemory[SessionEntity]):
    pass


@pytest.mark.asyncio
class TestRefreshSessionService:
    def setup_method(self):
        self.repository = SessionRepositoryInMemory()
        self.jwt = JWTAdapter()
        self.service = RefreshSessionService(self.repository, self.jwt)

        self.user_id = "811c5f65-c4e1-4084-8b15-e8342de5d57b"
        self.entity_session = SessionEntity({"user_id": self.user_id}).to_dict()

        current_time = int(datetime.now().timestamp())
        expires_in = 15 * 60
        self.token = self.jwt.encode(
            {
                "user_id": self.user_id,
                "session_id": self.entity_session["id"],
                "iat": current_time,
                "exp": current_time + expires_in,
            }
        )
        self.refresh_token = self.jwt.encode(
            {
                "session_id": self.entity_session["id"],
                "iat": self.entity_session["created_at"],
                "exp": self.entity_session["expires_at"],
            }
        )

    async def test_handle_exception_if_tokens_not_found(self):
        arrange = [
            None,
            {},
            {"access_token": self.token},
            {"refresh_token": self.refresh_token},
        ]

        for tokens in arrange:
            with pytest.raises(CustomError) as e:
                await self.service.handle({"tokens": tokens})

            custom_error = e.value
            assert custom_error.formate_errors == {
                "code_error": 400,
                "messages_error": ["Invalid access token or refresh token."],
            }

    async def test_handle_exception_if_access_token_not_match_refresh_token(self):
        wrong_token = self.jwt.encode(
            {
                "session_id": "wrong_user_id",
                "iat": self.entity_session["created_at"],
                "exp": self.entity_session["expires_at"],
            }
        )

        with pytest.raises(CustomError) as e:
            await self.service.handle(
                {
                    "tokens": {
                        "access_token": wrong_token,
                        "refresh_token": self.refresh_token,
                    }
                }
            )

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["Access token not match refresh token."],
        }

    async def test_handle_success(self):
        response = await self.service.handle(
            {
                "tokens": {
                    "access_token": self.token,
                    "refresh_token": self.refresh_token,
                }
            }
        )

        assert isinstance(response["access_token"], str)
        assert isinstance(response["refresh_token"], str)

        assert len(self.repository.list_data) == 1
        assert self.repository.list_data[0].to_dict()["user_id"] == self.user_id
