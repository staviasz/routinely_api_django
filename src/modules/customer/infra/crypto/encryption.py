from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

from modules.customer.contracts import EncryptionContract


class EncryptionAdapter(EncryptionContract):
    def __init__(self, crypto_secret_key: str):
        self.crypto_secret_key = crypto_secret_key.encode("utf-8")

    def encrypt(self, data: str) -> str:
        iv = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(self.crypto_secret_key),
            modes.GCM(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()

        encrypted = encryptor.update(data.encode("utf-8")) + encryptor.finalize()

        auth_tag = encryptor.tag

        return f"{iv.hex()}:{encrypted.hex()}:{auth_tag.hex()}"

    def decrypt(self, data: str) -> str:
        iv_hex, encrypted_hex, auth_tag_hex = data.split(":")
        iv = bytes.fromhex(iv_hex)
        encrypted = bytes.fromhex(encrypted_hex)
        auth_tag = bytes.fromhex(auth_tag_hex)

        cipher = Cipher(
            algorithms.AES(self.crypto_secret_key),
            modes.GCM(iv, auth_tag),
            backend=default_backend(),
        )
        decryptor = cipher.decryptor()

        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        return decrypted.decode("utf-8")
