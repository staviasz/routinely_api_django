from modules.customer.infra.crypto.encryption_to_send_email import (
    EncryptionToSendEmailAdapter,
)


class TestCrypto:
    def setup_method(self):
        self.crypto = EncryptionToSendEmailAdapter()

    def test_cryptography(self):
        data = "12345678901234567890123456789012"
        encrypted = self.crypto.encrypt(data)

        assert encrypted is not None
        assert encrypted != data
        decrypted = self.crypto.decrypt(encrypted)

        assert decrypted == data
