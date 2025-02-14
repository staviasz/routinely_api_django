from unittest.mock import patch

import pytest
from modules.customer.events.events_customer import CreatedCustomerEvent
from modules.customer.events.handles_customer import (
    SendEmailForgotPasswordCustomerHandler,
    SendEmailRegisterCustomerHandler,
)
from modules.mailing.adapter.mailing_adapter import MailingAdapter


@pytest.mark.asyncio
class TestSendEmailRegisterCustomerHandler:
    async def test_send_email_register_customer_handler(self):
        event = CreatedCustomerEvent()
        event.set_payload(
            {"email": "G0s7B@example.com", "callback_url": "http://localhost:3000"}
        )
        handler = SendEmailRegisterCustomerHandler()

        with patch.object(MailingAdapter, "send_email") as mock_perform:
            await handler.handle(event)
            mock_perform.assert_called_once()


@pytest.mark.asyncio
class TestSendEmailForgotPasswordCustomerHandler:
    async def test_send_email_forgot_password_customer_handler(self):
        event = CreatedCustomerEvent()
        event.set_payload(
            {"name": "Teste", "email": "G0s7B@example.com", "code": "123456"}
        )
        handler = SendEmailForgotPasswordCustomerHandler()

        with patch.object(MailingAdapter, "send_email") as mock_perform:
            await handler.handle(event)
            mock_perform.assert_called_once()
