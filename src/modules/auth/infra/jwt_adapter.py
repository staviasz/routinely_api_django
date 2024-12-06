import jwt
from main.configs import env
from modules.auth import JWTContract


class JWTAdapter(JWTContract):
    __secret_key = env["backend"]["secret_jwt"]
    __algorithm = "HS256"

    def encode(self, payload):
        return jwt.encode(payload, self.__secret_key, algorithm=self.__algorithm)

    def decode(self, token):
        return jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
