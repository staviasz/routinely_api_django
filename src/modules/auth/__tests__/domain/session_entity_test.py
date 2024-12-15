import pytest
from main.errors.shared.custom_error import CustomError
from modules.auth.domain.entity import SessionEntity


class TestSessionEntity:

    def test_raise_errors(self):
        with pytest.raises(CustomError) as e:
            SessionEntity({"user_id": None})

        custom_error = e.value
        assert custom_error.formate_errors == {
            "code_error": 400,
            "messages_error": ["The user id is required."],
        }

    def test_valid_entity(self):
        session = SessionEntity({"user_id": "1"})
        dict_session = session.to_dict()
        assert dict_session["user_id"] == "1"
        assert dict_session["created_at"] is not None
        assert dict_session["expires_at"] is not None
        assert dict_session["id"] is not None
