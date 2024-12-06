from typing import Protocol

from main.models import SendEmailModel


class MailingContract(Protocol):
    def send_email(self, props: SendEmailModel) -> None:
        pass
