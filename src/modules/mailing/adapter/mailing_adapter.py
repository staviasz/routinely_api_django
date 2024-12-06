from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import TypedDict

from main.models import SendEmailModel
from main.contracts import MailingContract


class InitProps(TypedDict):
    from_email: str
    password: str


class MailingAdapter(MailingContract):
    def __init__(self, props: InitProps) -> None:
        self.__email_sender = {
            "from_email": props["from_email"],
            "password": props["password"],
        }

    def send_email(self, props) -> None:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(
                self.__email_sender["from_email"], self.__email_sender["password"]
            )
            server.sendmail(
                self.__email_sender["from_email"],
                props["to_email"],
                self.__format_body_email(props),
            )
        finally:
            server.quit()

        return

    def __format_body_email(self, props: SendEmailModel) -> str:
        message = MIMEMultipart()
        message["From"] = self.__email_sender["from_email"]
        message["To"] = props["to_email"]
        message["Subject"] = props["subject"]
        message.attach(MIMEText(props["body"], "html"))
        return message.as_string()
