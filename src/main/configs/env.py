import os
from dotenv import load_dotenv
from typing import TypedDict


_env_path = ""
_python_env = os.getenv("PYTHON_ENV", "development")

match _python_env:
    case "development":
        _env_path = os.path.abspath(".env")
    case "production":
        _env_path = os.path.abspath(".env.production")
    case "test":
        _env_path = os.path.abspath(".env.test")

load_dotenv(dotenv_path=_env_path)


class SendEmailCustomer(TypedDict):
    smtp_port: int
    smtp_server: str
    from_email: str
    password: str
    secret_key_crypto: str


class Backend(TypedDict):
    port: int
    url: str
    private_key_jwt: str
    public_key_jwt: str
    secret_key_repository: str


class Database(TypedDict):
    engine: str
    name: str
    user: str
    password: str
    host: str
    port: int


class Framework(TypedDict):
    port: int
    allowed_host: list[str]
    secret_key: str
    debug: bool


class EnvTyped(TypedDict):
    env: str
    send_email_customer: SendEmailCustomer
    backend: Backend
    framework: Framework
    database: Database


env: EnvTyped = {
    "env": _python_env,
    "send_email_customer": {
        "from_email": os.getenv("SEND_EMAIL_CUSTOMER_FROM_EMAIL", ""),
        "password": os.getenv("SEND_EMAIL_CUSTOMER_PASSWORD", ""),
        "secret_key_crypto": os.getenv("SEND_EMAIL_CUSTOMER_SECRET_KEY_CRYPTO", ""),
        "smtp_server": os.getenv("SEND_EMAIL_CUSTOMER_SMTP_SERVER", ""),
        "smtp_port": int(os.getenv("SEND_EMAIL_CUSTOMER_SMTP_PORT", 0)),
    },
    "backend": {
        "port": int(os.getenv("PORT", 8000)),
        "url": os.getenv("BACKEND_URL", ""),
        "private_key_jwt": os.getenv("BACKEND_PRIVATE_KEY_JWT", ""),
        "public_key_jwt": os.getenv("BACKEND_PUBLIC_KEY_JWT", ""),
        "secret_key_repository": os.getenv("BACKEND_SECRET_KEY_REPOSITORY", ""),
    },
    "framework": {
        "port": int(os.getenv("PORT", 8000)),
        "allowed_host": os.getenv("ALLOWED_HOSTS", "").split(","),
        "secret_key": os.getenv("SECRET_KEY_FRAMEWORK", ""),
        "debug": bool(os.getenv("DEBUG", True)),
    },
    "database": {
        "engine": os.getenv("DATABASE_ENGINE", ""),
        "name": os.getenv("DATABASE_NAME", ""),
        "user": os.getenv("DATABASE_USER", ""),
        "password": os.getenv("DATABASE_PASSWORD", ""),
        "host": os.getenv("DATABASE_HOST", ""),
        "port": int(os.getenv("DATABASE_PORT", 0)),
    },
}
