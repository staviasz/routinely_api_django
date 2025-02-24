from unittest.mock import Mock

import pytest
from main.infra.base_validation_pydantic import BaseValidationPydantic
from modules.customer import (
    ConfirmEmailUsecaseContract,
    ConfirmEmailSchema,
    ConfirmEmailController,
    EncryptionContract,
)


@pytest.mark.asyncio
class TestConfirmEmailController:
    def setup_method(self):
        self.validator = BaseValidationPydantic(ConfirmEmailSchema)
        self.usecase = Mock(spec=ConfirmEmailUsecaseContract)
        self.crypto = Mock(spec=EncryptionContract)
        self.controller = ConfirmEmailController(
            self.validator, self.usecase, self.crypto
        )

    async def test_invalid_urls(self):
        arrange = [
            "example.com",
            "www.example.com",
            "sub.example.com/path",
            "ftp://example.com",
            "//example.com",
            "http://example..com",
            "http://example..org",
            "https://example.c",
            "https://.com",
            "https://com",
            "https://example..co.uk",
            "https://example._com",
            "https://exa_mple.com",
            "https://example.com path",
            "https:// example.com",
            "https://example. com",
            "https://example.com/pa ge",
            "https://example.com/# sect",
            "https://example!.com",
            "https://exa$mple.com",
            "https://example.com/<tag>",
            "https://example.com/|path",
            "https://example.com/\\path",
            "https://",
            "https://.",
            "https://example",
            "https://.example.com",
            "http://.co.uk",
        ]
        for url in arrange:
            str_query = f"any_email@test.com--{url}"
            query = {"": str_query}
            self.crypto.decrypt.return_value = str_query

            response = await self.controller.execute({"query": query})
            assert response["body"]["message"] == ["callback_url: Invalid URL"]
            assert response["status"] == 400

    async def test_invalid_email(self):
        arrange = [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@com",
            "username@domain..com",
            "username@domain,com",
            "username@domain.com (comment)",
            "username@domain..com",
            "username@.sub.domain.com",
            "user name@domain.com",
            "username@domain..com",
            "username@domain@domain.com",
            "username@domain.com.",
            "username@domain._com",
            "user@name@domain.com",
            "username@-domain.com",
            "username@domain.com-",
            "user@domain.com.",
            "username@domain.com..com",
            "username@domain.com!",
            "username@domain..com",
            "username@domain_com",
            "username@.com",
            "username@com.",
            "username@domain.123",
            "username@domain.a1",
            "username@.domain.com",
            "username@domain@domain.com",
        ]
        for email in arrange:
            str_query = f"{email}--http://localhost:3000"
            query = {"": str_query}
            self.crypto.decrypt.return_value = str_query

            response = await self.controller.execute({"query": query})
            assert response["status"] == 400

    async def test_success(self):
        str_query = "any_email@test.com--http://localhost:3000"
        query = {"": str_query}
        self.crypto.decrypt.return_value = str_query

        response = await self.controller.execute({"query": query})
        assert response["status"] == 302
        assert response["headers"]["Location"] == "http://localhost:3000"
