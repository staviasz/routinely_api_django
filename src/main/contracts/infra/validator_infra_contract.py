from typing import Protocol


class ValidatorContract(Protocol):
    def __init__(self) -> bool:
        pass
