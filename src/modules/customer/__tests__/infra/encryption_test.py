from modules.customer.infra.crypto.encryption import EncryptionAdapter


class Crypto(EncryptionAdapter):
    def __init__(self):
        super().__init__("12345678901234567890123456789012")


class TestCrypto:
    def setup_method(self):
        self.crypto = Crypto()

    def test_cryptography(self):
        data = "12345678901234567890123456789012"
        encrypted = self.crypto.encrypt(data)

        assert encrypted is not None
        assert encrypted != data
        decrypted = self.crypto.decrypt(encrypted)

        assert decrypted == data
