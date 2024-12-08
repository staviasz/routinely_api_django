from modules.auth.domain.entity import SessionEntity


class TestSessionEntity:
    def setup_method(self):
        self.entity = SessionEntity({"id": None, "token": "any_token"})

    def test_valid_entity(self):
        assert self.entity.to_dict() == {"id": None, "token": "any_token"}
