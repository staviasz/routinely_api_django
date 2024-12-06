from modules.auth.infra.jwt_adapter import JWTAdapter


class TestJWTAdapter:
    def setup_method(self):
        self.jwt = JWTAdapter()

    def test_encode_and_decode(self):
        payload = {"user_id": 1, " name": "John"}
        token = self.jwt.encode(payload)
        decoded_token = self.jwt.decode(token)

        assert token is not None
        assert type(token) is str

        assert decoded_token == payload
