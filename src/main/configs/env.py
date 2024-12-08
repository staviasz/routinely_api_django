import os
from dotenv import load_dotenv
from typing import TypedDict


_env_path = os.path.abspath(".env")
load_dotenv(dotenv_path=_env_path)


class SendEmailCustomer(TypedDict):
    from_email: str
    password: str
    secret_key_crypto: str


class Backend(TypedDict):
    port: int
    url: str
    private_key_jwt: str
    public_key_jwt: str


class EnvTyped(TypedDict):
    send_email_customer: SendEmailCustomer
    backend: Backend


env: EnvTyped = {
    "send_email_customer": {
        "from_email": os.getenv("SEND_EMAIL_CUSTOMER_FROM_EMAIL", ""),
        "password": os.getenv("SEND_EMAIL_CUSTOMER_PASSWORD", ""),
        "secret_key_crypto": os.getenv("SEND_EMAIL_CUSTOMER_SECRET_KEY_CRYPTO", ""),
    },
    "backend": {
        "port": int(os.getenv("BACKEND_PORT", 8080)),
        "url": os.getenv("BACKEND_URL", ""),
        "private_key_jwt": os.getenv("BACKEND_PRIVATE_KEY_JWT", ""),
        "public_key_jwt": os.getenv("BACKEND_PUBLIC_KEY_JWT", ""),
    },
}
