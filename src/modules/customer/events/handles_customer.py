import datetime
from main.contracts import HandlerContract, EventBaseClass
from modules.customer.infra import EncryptionToSendEmailAdapter
from modules.mailing.adapter import MailingAdapter
from main.configs import env
from modules.customer.templates import (
    register_customer_template,
    forget_password_template,
)
from main.utils import template_to_strings


class SendEmailRegisterCustomerHandler(HandlerContract):
    def __init__(self) -> None:
        self.__mailing = MailingAdapter(env["send_email_customer"])
        self.__template = register_customer_template
        self.__cryptography = EncryptionToSendEmailAdapter()
        self.__backend_url = env["backend"]["url"]

    def handle(self, event: EventBaseClass) -> None:
        email_customer = event.get_payload()["email"]
        callback_url = event.get_payload()["callback_url"]
        url = f"{self.__backend_url}/customer/confirm-email?{self.__cryptography.encrypt(f"{email_customer}-{callback_url}")}"
        year = datetime.date.today().year

        data = {
            "body": template_to_strings(self.__template, {"url": url, "year": year}),
            "to_email": email_customer,
            "subject": "Cadastro realizado com sucesso",
        }
        self.__mailing.send_email(data)


send_email_register_customer_handler = SendEmailRegisterCustomerHandler()


class SendEmailForgotPasswordCustomerHandler(HandlerContract):
    def __init__(self) -> None:
        self.__mailing = MailingAdapter(env["send_email_customer"])
        self.__template = forget_password_template

    def handle(self, event: EventBaseClass) -> None:
        event_payload = event.get_payload()
        name_customer = event_payload["name"]
        email_customer = event_payload["email"]
        code = event_payload["code"]

        data = {
            "body": template_to_strings(
                self.__template, {"name": name_customer, "code": code}
            ),
            "to_email": email_customer,
            "subject": "Recuperação de senha",
        }
        self.__mailing.send_email(data)


send_email_forgot_password_customer_handler = SendEmailForgotPasswordCustomerHandler()
