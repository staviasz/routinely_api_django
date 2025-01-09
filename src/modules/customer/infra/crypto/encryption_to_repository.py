from main.configs import env
from modules.customer.infra.crypto.encryption import EncryptionAdapter


class EncryptionToRepositoryAdapter(EncryptionAdapter):
    def __init__(self) -> None:
        super().__init__(env["backend"]["secret_key_repository"])
