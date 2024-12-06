from main.configs import env
from modules.customer.infra.crypto.encryption import EncryptionAdapter


class EncryptionToSendEmailAdapter(EncryptionAdapter):
    def __init__(self) -> None:
        super().__init__(env["send_email_customer"]["secret_key_crypto"])
