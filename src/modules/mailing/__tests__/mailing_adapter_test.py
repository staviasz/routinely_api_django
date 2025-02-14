import unittest
from unittest.mock import patch, MagicMock
from main.configs import env
from modules.mailing.adapter import MailingAdapter


class TestMailingAdapter(unittest.TestCase):
    def setUp(self):
        self.init_props = {
            "smtp_server": env["send_email_customer"]["smtp_server"],
            "smtp_port": env["send_email_customer"]["smtp_port"],
            "from_email": "test.sender@example.com",
            "password": "password123",
        }

        self.adapter = MailingAdapter(self.init_props)

        self.email_props = {
            "to_email": "test.recipient@example.com",
            "subject": "Test Email",
            "body": "<p>This is a test email.</p>",
        }

    @patch("smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        self.adapter.send_email(self.email_props)

        mock_smtp.assert_called_once_with(
            self.init_props["smtp_server"], self.init_props["smtp_port"]
        )
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(
            self.init_props["from_email"], self.init_props["password"]
        )

        args, kwargs = mock_server.sendmail.call_args
        self.assertEqual(args[0], self.init_props["from_email"])  # From
        self.assertEqual(args[1], self.email_props["to_email"])  # To

        email_body = args[2]
        self.assertIn("From: test.sender@example.com", email_body)
        self.assertIn("To: test.recipient@example.com", email_body)
        self.assertIn("Subject: Test Email", email_body)
        self.assertIn("<p>This is a test email.</p>", email_body)

        mock_server.quit.assert_called_once()

    def test_format_body_email(self):
        """Testa o método de formatação do corpo do e-mail."""
        formatted_body = self.adapter._MailingAdapter__format_body_email(
            self.email_props
        )

        # Verifica se os campos estão presentes no corpo formatado
        self.assertIn("From: test.sender@example.com", formatted_body)
        self.assertIn("To: test.recipient@example.com", formatted_body)
        self.assertIn("Subject: Test Email", formatted_body)
        self.assertIn("<p>This is a test email.</p>", formatted_body)
