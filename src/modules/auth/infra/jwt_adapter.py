import jwt
from main.configs import env
from modules.auth import JWTContract


class JWTAdapter(JWTContract):
    __private_key = env["backend"]["private_key_jwt"]
    __public_key = env["backend"]["public_key_jwt"]
    __algorithm = "RS256"

    def encode(self, payload):
        return jwt.encode(payload, self.__private_key, algorithm=self.__algorithm)

    def decode(self, token):
        return jwt.decode(token, self.__public_key, algorithms=[self.__algorithm])
