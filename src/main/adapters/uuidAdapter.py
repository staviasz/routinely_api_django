import uuid


class UuidAdapter:

    @staticmethod
    def generate_uuid4() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def validate_uuid4(id: str) -> bool:
        try:
            uuid_obj = uuid.UUID(id)
            return str(uuid_obj) == id
        except ValueError:
            return False
