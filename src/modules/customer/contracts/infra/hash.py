from typing import Protocol


class HashContract(Protocol):
    def hash(self, text: str) -> str:
        pass

    def verify(self, text: str, hashed_text: str) -> bool:
        pass
