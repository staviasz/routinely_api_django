from unittest.mock import Mock, patch

import pytest

from modules.auth.contracts.services.session_service_contract import (
    SessionServiceContract,
)
from modules.customer.app.usecases.refresh_login_usecase import RefreshLoginUsecase


@pytest.mark.asyncio
class TestRefreshLoginUsecase:
    def setup_method(self):
        self.auth = Mock(spec=SessionServiceContract)
        self.usecase = RefreshLoginUsecase(self.auth)

    async def test_refresh_login_usecase(self):
        props = {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
        }
        expect = {
            "access_token": "access_token_update",
            "refresh_token": "refresh_token_update",
            "expires_in": 3600,
        }
        with patch.object(self.auth, "handle") as mock_auth:

            self.auth.handle.return_value = expect
            response = await self.usecase.perform(props)

            mock_auth.assert_called_once_with({"tokens": props})
            assert response == expect
