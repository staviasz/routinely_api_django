from typing import Protocol


class EncryptionContract(Protocol):
    def encrypt(self, password: str) -> str:
        pass

    def decrypt(self, password: str) -> str:
        pass
