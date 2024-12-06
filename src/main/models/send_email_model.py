from typing import TypedDict


class SendEmailModel(TypedDict):
    to_email: str
    subject: str
    body: str
