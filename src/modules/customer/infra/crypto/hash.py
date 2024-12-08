import bcrypt
from modules.customer.contracts import HashContract


class HashAdapter(HashContract):
    def hash(self, text: str) -> str:
        text_hash = bcrypt.hashpw(text.encode("utf-8"), bcrypt.gensalt())
        return text_hash.decode("utf-8")

    def verify(self, text: str, hashed_text: str) -> bool:
        return bcrypt.checkpw(text.encode("utf-8"), hashed_text.encode("utf-8"))
